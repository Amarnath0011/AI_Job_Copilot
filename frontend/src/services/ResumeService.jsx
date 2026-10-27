import api from "../api/axios";

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  // Let Axios/browser set the multipart boundary automatically.
  const response = await api.post("/resume/upload", formData);
  return response.data;
};
