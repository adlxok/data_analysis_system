import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Django后端API的基础URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 获取招聘列表数据
export const getJobList = async (params = {}) => {
  try {
    const response = await api.get('job_postings/', { params });
    return response.data;
  } catch (error) {
    console.error('获取招聘列表失败:', error);
    throw error;
  }
};

// 获取单个招聘详情
export const getJobDetail = async (id) => {
  try {
    const response = await api.get(`job_postings/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`获取招聘ID: ${id} 详情失败:`, error);
    throw error;
  }
};

export default {
  getJobList,
  getJobDetail,
};