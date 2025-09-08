import Link from 'next/link'
import Navbar from '@/components/Navbar'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navbar />
      
      {/* 히어로 섹션 */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                게시판
              </span>
              <br />
              <span className="text-gray-700">애플리케이션</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              FastAPI + Next.js로 구축된 현대적인 게시판 서비스
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/posts"
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
              >
                게시판 바로가기
              </Link>
              <Link
                href="/register"
                className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl text-lg font-semibold hover:border-blue-500 hover:text-blue-600 transition-all duration-300"
              >
                회원가입
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* 기능 소개 섹션 */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              주요 기능
            </h2>
            <p className="text-xl text-gray-600">
              사용자 친화적인 인터페이스와 강력한 기능들
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl p-8 transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <span className="text-2xl">📝</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                게시글 관리
              </h3>
              <p className="text-gray-600 leading-relaxed">
                직관적인 에디터로 게시글을 작성하고, 수정하며, 삭제할 수 있습니다.
              </p>
            </div>
            
            <div className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl p-8 transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <span className="text-2xl">💬</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                댓글 시스템
              </h3>
              <p className="text-gray-600 leading-relaxed">
                실시간 댓글 작성과 관리로 활발한 소통을 지원합니다.
              </p>
            </div>
            
            <div className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl p-8 transition-all duration-300 transform hover:-translate-y-2 border border-gray-100">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <span className="text-2xl">👤</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                사용자 인증
              </h3>
              <p className="text-gray-600 leading-relaxed">
                안전한 회원가입과 로그인으로 개인화된 서비스를 제공합니다.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* AI 기능 준비 섹션 */}
      <div className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-white/10 backdrop-blur-sm rounded-3xl p-12 border border-white/20">
            <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-8">
              <span className="text-4xl">🚀</span>
            </div>
            <h3 className="text-3xl md:text-4xl font-bold text-white mb-6">
              AI 기능 준비 중
            </h3>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              곧 AI 기반의 스마트한 기능들이 추가될 예정입니다!
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-white/80">
              <span className="bg-white/20 px-4 py-2 rounded-full text-sm">자동 번역</span>
              <span className="bg-white/20 px-4 py-2 rounded-full text-sm">스마트 검색</span>
              <span className="bg-white/20 px-4 py-2 rounded-full text-sm">콘텐츠 추천</span>
              <span className="bg-white/20 px-4 py-2 rounded-full text-sm">감정 분석</span>
            </div>
          </div>
        </div>
      </div>

      {/* 푸터 */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            © 2024 게시판 애플리케이션. FastAPI + Next.js로 구축되었습니다.
          </p>
        </div>
      </footer>
    </div>
  );
}

