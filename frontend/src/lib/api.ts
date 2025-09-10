const API_BASE_URL = 'http://localhost:8000/api/v1';

// API 클라이언트 클래스
class ApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  // 인증 API
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(error.detail || 'Login failed');
    }

    const data = await response.json();
    this.setToken(data.access_token);
    return data;
  }

  async register(username: string, email: string, password: string, confirm_password: string) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        username,
        email,
        password,
        confirm_password,
      }),
    });
  }

  // 사용자 API
  async getCurrentUser() {
    return this.request('/users/me');
  }

  async updateUser(userData: any) {
    return this.request('/users/me', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  // 게시글 API
  async getPosts(page: number = 1, size: number = 10) {
    return this.request(`/posts/?page=${page}&size=${size}`);
  }

  async getPost(postId: number) {
    return this.request(`/posts/${postId}`);
  }

  async createPost(title: string, content: string) {
    return this.request('/posts/', {
      method: 'POST',
      body: JSON.stringify({ title, content }),
    });
  }

  async updatePost(postId: number, title: string, content: string) {
    return this.request(`/posts/${postId}`, {
      method: 'PUT',
      body: JSON.stringify({ title, content }),
    });
  }

  async deletePost(postId: number) {
    return this.request(`/posts/${postId}`, {
      method: 'DELETE',
    });
  }

  // 댓글 API
  async getComments(postId: number) {
    return this.request(`/posts/${postId}/comments`);
  }

  async createComment(postId: number, content: string) {
    return this.request('/comments/', {
      method: 'POST',
      body: JSON.stringify({ post_id: postId, content }),
    });
  }

  async updateComment(commentId: number, content: string) {
    return this.request(`/comments/${commentId}`, {
      method: 'PUT',
      body: JSON.stringify({ content }),
    });
  }

  async deleteComment(commentId: number) {
    return this.request(`/comments/${commentId}`, {
      method: 'DELETE',
    });
  }

  // AI 관련 API
  async getColumnCandidates(input: string, topK: number = 5) {
    return this.request('/ai/column-candidates', {
      method: 'POST',
      body: JSON.stringify({
        input,
        top_k: topK,
      }),
    });
  }

  async updateEmbeddings() {
    return this.request('/ai/update-embeddings', {
      method: 'POST',
    });
  }

  async getAIHealth() {
    return this.request('/ai/health', {
      method: 'GET',
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
