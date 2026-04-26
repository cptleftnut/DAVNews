"""Google Drive uploader – authenticates via a Service Account and uploads
the rendered video into a 'DAVNews' folder (created if missing).
"""

import os

from core.config import settings

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    _GOOGLE_AVAILABLE = True
except ImportError:
    _GOOGLE_AVAILABLE = False


SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _get_drive_service():
    """Return an authenticated Google Drive API service instance."""
    creds = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_APPLICATION_CREDENTIALS,
        scopes=SCOPES,
    )
    return build("drive", "v3", credentials=creds)


def _find_or_create_folder(service, folder_name: str) -> str:
    """Locate a folder by name in Drive; create it if it doesn't exist.

    Returns the folder's Drive file ID.
    """
    query = (
        f"name='{folder_name}' "
        "and mimeType='application/vnd.google-apps.folder' "
        "and trashed=false"
    )
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    # Create the folder
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=metadata, fields="id").execute()
    return folder["id"]


def upload_to_drive(file_path: str) -> str:
    """Upload *file_path* to the 'DAVNews' folder in Google Drive.

    Returns a shareable web link to the uploaded file.  When Google
    credentials are not configured, returns a placeholder URL so the
    pipeline can continue without crashing.
    """
    if not _GOOGLE_AVAILABLE:
        return f"https://drive.google.com/placeholder/{os.path.basename(file_path)}"

    creds_path = settings.GOOGLE_APPLICATION_CREDENTIALS
    if not os.path.isfile(creds_path):
        return f"https://drive.google.com/placeholder/{os.path.basename(file_path)}"

    try:
        service = _get_drive_service()
        folder_id = _find_or_create_folder(service, settings.GDRIVE_FOLDER_NAME)

        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [folder_id],
        }
        media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)
        uploaded = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id, webViewLink")
            .execute()
        )

        # Make the file accessible via link
        service.permissions().create(
            fileId=uploaded["id"],
            body={"type": "anyone", "role": "reader"},
        ).execute()

        return uploaded.get(
            "webViewLink",
            f"https://drive.google.com/file/d/{uploaded['id']}/view",
        )
    except Exception as exc:
        return f"https://drive.google.com/error?reason={exc}"
