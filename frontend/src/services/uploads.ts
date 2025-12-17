import { api } from './api';

export interface UploadImageResponse {
  success: boolean;
  filename: string;
  url: string;
  size: number;
}

export const uploadService = {
  uploadImage: async (file: File): Promise<UploadImageResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<UploadImageResponse>(
      '/api/v1/uploads/image',
      formData,
      {
        headers: { 'Content-Type': 'multipart/form-data' },
      }
    );

    return response.data;
  },
};

