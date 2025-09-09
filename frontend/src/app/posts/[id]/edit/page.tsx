'use client'

import { useState, useEffect } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import Navbar from '@/components/Navbar'

interface Post {
  id: number
  title: string
  content: string
  user_id: number
  view_count: number
  created_at: string
  updated_at: string | null
}

export default function EditPostPage() {
  const [post, setPost] = useState<Post | null>(null)
  const [formData, setFormData] = useState({
    title: '',
    content: ''
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [updateLoading, setUpdateLoading] = useState(false)
  const { user } = useAuth()
  const router = useRouter()
  const params = useParams()
  const postId = params.id as string

  useEffect(() => {
    if (postId) {
      fetchPost()
    }
  }, [postId])

  const fetchPost = async () => {
    try {
      const data = await apiClient.getPost(parseInt(postId))
      setPost(data)
      setFormData({
        title: data.title,
        content: data.content
      })
    } catch (err: any) {
      setError(err.message || '게시글을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setUpdateLoading(true)
    setError('')

    try {
      await apiClient.updatePost(parseInt(postId), formData.title, formData.content)
      router.push(`/posts/${postId}`)
    } catch (err: any) {
      setError(err.message || '게시글 수정에 실패했습니다.')
    } finally {
      setUpdateLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
      return
    }

    setUpdateLoading(true)
    setError('')

    try {
      await apiClient.deletePost(parseInt(postId))
      router.push('/posts')
    } catch (err: any) {
      setError(err.message || '게시글 삭제에 실패했습니다.')
    } finally {
      setUpdateLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Navbar />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">게시글을 불러오는 중...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!user || !post || user.id !== post.user_id) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Navbar />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <div className="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-4xl text-red-400">🚫</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              접근 권한이 없습니다
            </h3>
            <p className="text-gray-600 mb-6">
              본인이 작성한 게시글만 수정할 수 있습니다.
            </p>
            <Link
              href="/posts"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              게시판으로 돌아가기
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 헤더 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                게시글 수정
              </h1>
              <p className="text-gray-600">
                게시글을 수정하거나 삭제할 수 있습니다
              </p>
            </div>
            <Link
              href={`/posts/${postId}`}
              className="text-gray-600 hover:text-blue-600 transition-colors"
            >
              ← 게시글 보기
            </Link>
          </div>
        </div>

        {/* 게시글 수정 폼 */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-2">
                제목
              </label>
              <input
                id="title"
                name="title"
                type="text"
                required
                value={formData.title}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
                placeholder="게시글 제목을 입력하세요"
              />
            </div>

            <div>
              <label htmlFor="content" className="block text-sm font-semibold text-gray-700 mb-2">
                내용
              </label>
              <textarea
                id="content"
                name="content"
                required
                rows={12}
                value={formData.content}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 resize-none"
                placeholder="게시글 내용을 입력하세요"
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm flex items-center">
                <span className="mr-2">⚠️</span>
                {error}
              </div>
            )}

            <div className="flex justify-between">
              <button
                type="button"
                onClick={handleDelete}
                disabled={updateLoading}
                className="bg-red-500 text-white px-6 py-3 rounded-xl font-semibold hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                {updateLoading ? '삭제 중...' : '게시글 삭제'}
              </button>
              
              <div className="flex space-x-4">
                <Link
                  href={`/posts/${postId}`}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl font-semibold hover:border-blue-500 hover:text-blue-600 transition-all duration-200"
                >
                  취소
                </Link>
                <button
                  type="submit"
                  disabled={updateLoading}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
                >
                  {updateLoading ? '저장 중...' : '수정 완료'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
