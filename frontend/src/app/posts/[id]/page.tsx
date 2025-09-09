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

interface Comment {
  id: number
  content: string
  user_id: number
  post_id: number
  created_at: string
  updated_at: string | null
}

export default function PostDetailPage() {
  const [post, setPost] = useState<Post | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [commentContent, setCommentContent] = useState('')
  const [commentLoading, setCommentLoading] = useState(false)
  const [editingComment, setEditingComment] = useState<number | null>(null)
  const [editCommentContent, setEditCommentContent] = useState('')
  const { user } = useAuth()
  const router = useRouter()
  const params = useParams()
  const postId = params.id as string

  useEffect(() => {
    if (postId) {
      fetchPost()
      fetchComments()
    }
  }, [postId])

  const fetchPost = async () => {
    try {
      const data = await apiClient.getPost(parseInt(postId))
      setPost(data)
    } catch (err: any) {
      setError(err.message || '게시글을 불러오는데 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const fetchComments = async () => {
    try {
      const data = await apiClient.getComments(parseInt(postId))
      setComments(data)
    } catch (err: any) {
      console.error('댓글을 불러오는데 실패했습니다:', err)
    }
  }

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user) {
      setError('로그인이 필요합니다.')
      return
    }

    setCommentLoading(true)
    try {
      await apiClient.createComment(parseInt(postId), commentContent)
      setCommentContent('')
      fetchComments() // 댓글 목록 새로고침
    } catch (err: any) {
      setError(err.message || '댓글 작성에 실패했습니다.')
    } finally {
      setCommentLoading(false)
    }
  }

  const handleEditComment = (comment: Comment) => {
    setEditingComment(comment.id)
    setEditCommentContent(comment.content)
  }

  const handleUpdateComment = async (commentId: number) => {
    setCommentLoading(true)
    try {
      await apiClient.updateComment(commentId, editCommentContent)
      setEditingComment(null)
      setEditCommentContent('')
      fetchComments()
    } catch (err: any) {
      setError(err.message || '댓글 수정에 실패했습니다.')
    } finally {
      setCommentLoading(false)
    }
  }

  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
      return
    }

    setCommentLoading(true)
    try {
      await apiClient.deleteComment(commentId)
      fetchComments()
    } catch (err: any) {
      setError(err.message || '댓글 삭제에 실패했습니다.')
    } finally {
      setCommentLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
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

  if (error || !post) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Navbar />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <div className="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <span className="text-4xl text-red-400">⚠️</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              게시글을 찾을 수 없습니다
            </h3>
            <p className="text-gray-600 mb-6">
              {error || '요청하신 게시글이 존재하지 않습니다.'}
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
        {/* 네비게이션 */}
        <div className="mb-6">
          <Link
            href="/posts"
            className="text-gray-600 hover:text-blue-600 transition-colors flex items-center"
          >
            ← 게시판으로 돌아가기
          </Link>
        </div>

        {/* 게시글 내용 */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 mb-8">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              {post.title}
            </h1>
            
            <div className="flex items-center justify-between text-sm text-gray-500 mb-6">
              <div className="flex items-center space-x-4">
                <span className="flex items-center">
                  <span className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-2">
                    <span className="text-white text-sm font-bold">
                      U
                    </span>
                  </span>
                  사용자 {post.user_id}
                </span>
                <span>•</span>
                <span>{formatDate(post.created_at)}</span>
                <span>•</span>
                <span>조회 {post.view_count}</span>
              </div>
              
              {user && user.id === post.user_id && (
                <div className="flex space-x-2">
                  <Link
                    href={`/posts/${post.id}/edit`}
                    className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                  >
                    수정
                  </Link>
                </div>
              )}
            </div>
          </div>

          <div className="prose max-w-none">
            <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {post.content}
            </div>
          </div>
        </div>

        {/* 댓글 섹션 */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            댓글 ({comments.length})
          </h2>

          {/* 댓글 작성 폼 */}
          {user ? (
            <form onSubmit={handleCommentSubmit} className="mb-8">
              <div className="mb-4">
                <textarea
                  value={commentContent}
                  onChange={(e) => setCommentContent(e.target.value)}
                  placeholder="댓글을 작성해주세요..."
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 resize-none"
                  required
                />
              </div>
              <div className="flex justify-end">
                <button
                  type="submit"
                  disabled={commentLoading}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {commentLoading ? '작성 중...' : '댓글 작성'}
                </button>
              </div>
            </form>
          ) : (
            <div className="mb-8 p-4 bg-gray-50 rounded-xl text-center">
              <p className="text-gray-600 mb-2">댓글을 작성하려면 로그인이 필요합니다.</p>
              <Link
                href="/login"
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                로그인하기
              </Link>
            </div>
          )}

          {/* 댓글 목록 */}
          {comments.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              아직 댓글이 없습니다. 첫 번째 댓글을 작성해보세요!
            </div>
          ) : (
            <div className="space-y-4">
              {comments.map((comment) => (
                <div
                  key={comment.id}
                  className="border-b border-gray-200 pb-4 last:border-b-0"
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <span className="text-white text-sm font-bold">
                        U
                      </span>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center space-x-2">
                          <span className="font-medium text-gray-900">
                            사용자 {comment.user_id}
                          </span>
                          <span className="text-gray-400">•</span>
                          <span className="text-sm text-gray-500">
                            {formatDate(comment.created_at)}
                          </span>
                        </div>
                        
                        {user && user.id === comment.user_id && (
                          <div className="flex space-x-2">
                            {editingComment === comment.id ? (
                              <>
                                <button
                                  onClick={() => handleUpdateComment(comment.id)}
                                  disabled={commentLoading}
                                  className="text-green-600 hover:text-green-700 text-sm font-medium"
                                >
                                  저장
                                </button>
                                <button
                                  onClick={() => setEditingComment(null)}
                                  className="text-gray-600 hover:text-gray-700 text-sm font-medium"
                                >
                                  취소
                                </button>
                              </>
                            ) : (
                              <>
                                <button
                                  onClick={() => handleEditComment(comment)}
                                  className="text-blue-600 hover:text-blue-700 text-sm font-medium"
                                >
                                  수정
                                </button>
                                <button
                                  onClick={() => handleDeleteComment(comment.id)}
                                  className="text-red-600 hover:text-red-700 text-sm font-medium"
                                >
                                  삭제
                                </button>
                              </>
                            )}
                          </div>
                        )}
                      </div>
                      
                      {editingComment === comment.id ? (
                        <textarea
                          value={editCommentContent}
                          onChange={(e) => setEditCommentContent(e.target.value)}
                          rows={3}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 resize-none"
                        />
                      ) : (
                        <p className="text-gray-800 whitespace-pre-wrap">
                          {comment.content}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
