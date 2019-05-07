import os
import zipfile
from collections import OrderedDict

import click
import progressbar
import requests
from requests_toolbelt.multipart import encoder
from paperspace import logger as default_logger

from paperspace.exceptions import S3UploadFailedException, PresignedUrlUnreachableException, \
    PresignedUrlAccessDeniedException, PresignedUrlConnectionException, ProjectAccessDeniedException


class S3WorkspaceHandler:
    def __init__(self, experiments_api, logger=None):
        """

        :param experiments_api: paperspace.client.API
        :param logger: paperspace.logger
        """
        self.experiments_api = experiments_api
        self.logger = logger or default_logger

    def _retrieve_file_paths(self, dirName):
        # setup file paths variable
        file_paths = {}
        exclude = ['.git', '.idea', '.pytest_cache']
        # Read all directory, subdirectories and file lists
        for root, dirs, files in os.walk(dirName, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for filename in files:
                # Create the full filepath by using os module.
                relpath = os.path.relpath(root, dirName)
                if relpath == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, dirName), filename)
                file_paths[file_path] = os.path.join(root, filename)

        # return all paths
        return file_paths

    def _zip_workspace(self, workspace_path):
        if not workspace_path:
            workspace_path = '.'
            zip_file_name = os.path.basename(os.getcwd()) + '.zip'
        else:
            zip_file_name = os.path.basename(workspace_path) + '.zip'

        zip_file_path = os.path.join(workspace_path, zip_file_name)

        if os.path.exists(zip_file_path):
            self.logger.log('Removing existing archive')
            os.remove(zip_file_path)

        file_paths = self._retrieve_file_paths(workspace_path)

        self.logger.log('Creating zip archive: %s' % zip_file_name)
        zip_file = zipfile.ZipFile(zip_file_path, 'w')

        bar = progressbar.ProgressBar(max_value=len(file_paths))

        with zip_file:
            i = 0
            for relpath, abspath in file_paths.items():
                i += 1
                self.logger.debug('Adding %s to archive' % relpath)
                zip_file.write(abspath, arcname=relpath)
                bar.update(i)
        bar.finish()
        self.logger.log('\nFinished creating archive: %s' % zip_file_name)
        return zip_file_path

    def _create_callback(self, encoder_obj):
        bar = progressbar.ProgressBar(max_value=encoder_obj.len)

        def callback(monitor):
            bar.update(monitor.bytes_read)

        return callback

    def upload_workspace(self, input_data):
        workspace_url = input_data.get('workspaceUrl')
        workspace_path = input_data.get('workspace')
        workspace_archive = input_data.get('workspaceArchive')
        if (workspace_archive and workspace_path) or (workspace_archive and workspace_url) or (
                workspace_path and workspace_url):
            raise click.UsageError("Use either:\n\t--workspaceUrl to point repository URL"
                                   "\n\t--workspace to point on project directory"
                                   "\n\t--workspaceArchive to point on project .zip archive"
                                   "\n or neither to use current directory")

        if workspace_url:
            return  # nothing to do

        if workspace_archive:
            archive_path = os.path.abspath(workspace_archive)
        else:
            archive_path = self._zip_workspace(workspace_path)

        file_name = os.path.basename(archive_path)
        project_handle = input_data['projectHandle']

        s3_upload_data = self._get_upload_data(file_name, project_handle)

        bucket_name = s3_upload_data['bucket_name']
        s3_object_path = s3_upload_data['fields']['key']

        self.logger.log('Uploading zipped workspace to S3')

        self._upload(archive_path, s3_upload_data)

        self.logger.log('\nUploading completed')

        return 's3://{}/{}'.format(bucket_name, s3_object_path)

    def _upload(self, archive_path, s3_upload_data):
        files = {'file': (archive_path, open(archive_path, 'rb'))}
        fields = OrderedDict(s3_upload_data['fields'])
        fields.update(files)

        s3_encoder = encoder.MultipartEncoder(fields=fields)
        monitor = encoder.MultipartEncoderMonitor(s3_encoder, callback=self._create_callback(s3_encoder))
        s3_response = requests.post(s3_upload_data['url'], data=monitor, headers={'Content-Type': monitor.content_type})
        self.logger.debug("S3 upload response: {}".format(s3_response.headers))
        if not s3_response.ok:
            raise S3UploadFailedException(s3_response)

    def _get_upload_data(self, file_name, project_handle):
        response = self.experiments_api.get("/workspace/get_presigned_url",
                                            params={'workspaceName': file_name, 'projectHandle': project_handle})
        if response.status_code == 401:
            raise ProjectAccessDeniedException(project_handle)
        if response.status_code == 403:
            raise PresignedUrlAccessDeniedException
        if response.status_code == 404:
            raise PresignedUrlUnreachableException
        if not response.ok:
            raise PresignedUrlConnectionException(response.reason)
        return response.json()
