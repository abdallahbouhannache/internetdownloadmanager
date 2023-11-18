// export const CATEGORY_TYPES = {
//     COMPRESSED: 'compressed',
//     DOCUMENT: 'document',
//     VIDEO: 'video',
//     AUDIO: 'audio',
//     UNKNOWN: 'unknown',
//   } as const;
  
export  const CATEGORY_TYPES = {
    COMPRESSED: ['zip', 'rar', '7z', 'tar', 'gz'],
    DOCUMENT: ['doc', 'docx', 'pdf', 'txt', 'xls', 'xlsx', 'ppt', 'pptx'],
    VIDEO: ['mp4', 'mkv', 'flv', 'avi', 'mov', 'wmv'],
    AUDIO: ['mp3', 'wav', 'aac', 'flac', 'ogg'],
    EXECUTABLE: ['exe'],
    UNKNOWN: []
} as const;

export const Status_Download={
    Pending: "pending",
    Downloading: "downloading",
    Completed: "completed",
    Error: "error"
}

  