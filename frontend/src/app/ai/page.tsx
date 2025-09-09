'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import Navbar from '@/components/Navbar'

interface ColumnCandidate {
  column_name: string
  similarity: number
  description: string
}

interface AIResponse {
  candidates: string[]
  details: ColumnCandidate[]
  input: string
  message?: string
}

export default function AIPage() {
  const [input, setInput] = useState('')
  const [topK, setTopK] = useState(5)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<AIResponse | null>(null)
  const [aiHealth, setAIHealth] = useState<any>(null)
  const [embeddingLoading, setEmbeddingLoading] = useState(false)
  const { user } = useAuth()

  useEffect(() => {
    checkAIHealth()
  }, [])

  const checkAIHealth = async () => {
    try {
      const health = await apiClient.getAIHealth()
      setAIHealth(health)
    } catch (err: any) {
      console.error('AI 상태 확인 실패:', err)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) {
      setError('입력값을 입력해주세요.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await apiClient.getColumnCandidates(input, topK)
      setResult(response)
    } catch (err: any) {
      setError(err.message || '컬럼 후보 추출에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateEmbeddings = async () => {
    setEmbeddingLoading(true)
    setError('')

    try {
      const response = await apiClient.updateEmbeddings()
      alert(`✅ ${response.message}\n총 ${response.count}개의 임베딩이 생성되었습니다.`)
      checkAIHealth() // 상태 새로고침
    } catch (err: any) {
      setError(err.message || '임베딩 갱신에 실패했습니다.')
    } finally {
      setEmbeddingLoading(false)
    }
  }

  const formatSimilarity = (similarity: number) => {
    return (similarity * 100).toFixed(1)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 헤더 */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🤖 AI 컬럼 후보 추출
          </h1>
          <p className="text-gray-600">
            자연어 입력을 통해 관련된 데이터베이스 컬럼을 찾아보세요
          </p>
        </div>

        {/* AI 상태 */}
        {aiHealth && (
          <div className="mb-6">
            <div className={`p-4 rounded-xl border ${
              aiHealth.status === 'healthy' 
                ? 'bg-green-50 border-green-200' 
                : 'bg-red-50 border-red-200'
            }`}>
              <div className="flex items-center">
                <span className="text-2xl mr-3">
                  {aiHealth.status === 'healthy' ? '✅' : '❌'}
                </span>
                <div>
                  <h3 className="font-semibold text-gray-900">
                    AI 서비스 상태: {aiHealth.status === 'healthy' ? '정상' : '오류'}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {aiHealth.message}
                  </p>
                  {aiHealth.model_loaded && (
                    <p className="text-xs text-gray-500 mt-1">
                      임베딩 차원: {aiHealth.embedding_dimension}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* 입력 폼 */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              📝 입력
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="input" className="block text-sm font-semibold text-gray-700 mb-2">
                  자연어 입력
                </label>
                <textarea
                  id="input"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50 resize-none"
                  placeholder="예: 매출이 높은 사용자 찾기, 기부 금액이 많은 후원자, 최근 기부한 사람들..."
                />
              </div>

              <div>
                <label htmlFor="topK" className="block text-sm font-semibold text-gray-700 mb-2">
                  상위 결과 개수
                </label>
                <select
                  id="topK"
                  value={topK}
                  onChange={(e) => setTopK(parseInt(e.target.value))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50"
                >
                  <option value={3}>3개</option>
                  <option value={5}>5개</option>
                  <option value={10}>10개</option>
                </select>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm">
                  ⚠️ {error}
                </div>
              )}

              <div className="flex space-x-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {loading ? '분석 중...' : '🔍 컬럼 후보 추출'}
                </button>
              </div>
            </form>

            {/* 임베딩 갱신 버튼 */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">
                🔄 임베딩 관리
              </h3>
              <button
                onClick={handleUpdateEmbeddings}
                disabled={embeddingLoading}
                className="w-full bg-orange-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                {embeddingLoading ? '임베딩 생성 중...' : '임베딩 갱신'}
              </button>
              <p className="text-xs text-gray-500 mt-2">
                컬럼 설명이 변경되었을 때 임베딩을 다시 생성합니다
              </p>
            </div>
          </div>

          {/* 결과 */}
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              🎯 결과
            </h2>

            {result ? (
              <div className="space-y-4">
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">입력:</h3>
                  <p className="text-blue-800">"{result.input}"</p>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">추출된 컬럼 후보:</h3>
                  <div className="space-y-3">
                    {result.details.map((detail, index) => (
                      <div
                        key={detail.column_name}
                        className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-xl p-4"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-semibold text-gray-900">
                            #{index + 1} {detail.column_name}
                          </span>
                          <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-medium">
                            {formatSimilarity(detail.similarity)}% 일치
                          </span>
                        </div>
                        <p className="text-sm text-gray-600">
                          {detail.description}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                {result.message && (
                  <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-xl text-sm">
                    💡 {result.message}
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🤖</span>
                </div>
                <p>입력값을 입력하고 분석 버튼을 클릭하세요</p>
              </div>
            )}
          </div>
        </div>

        {/* 사용 예시 */}
        <div className="mt-8 bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            💡 사용 예시
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h3 className="font-semibold text-gray-700">입력 예시:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• "매출이 높은 사용자"</li>
                <li>• "기부 금액이 많은 후원자"</li>
                <li>• "최근 기부한 사람들"</li>
                <li>• "기부 목적별 분류"</li>
                <li>• "결제 방법 확인"</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-gray-700">예상 결과:</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• amount (기부 금액)</li>
                <li>• donor_name (기부자 이름)</li>
                <li>• donation_date (기부 날짜)</li>
                <li>• purpose (기부 목적)</li>
                <li>• payment_method (결제 방법)</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
