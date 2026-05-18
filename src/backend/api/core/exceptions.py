class AppError(Exception):
    pass

class InvalidUrlError(AppError):
    pass

class DownloadError(AppError):
    pass

class FileSystemError(AppError):
    pass
