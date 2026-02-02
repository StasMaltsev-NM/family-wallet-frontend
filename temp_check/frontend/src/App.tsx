import { useEffect, useState } from 'react'
import './App.css'

interface TelegramWebApp {
  initData: string
  initDataUnsafe: {
    user?: {
      id: number
      first_name: string
      last_name?: string
      username?: string
      language_code?: string
      is_premium?: boolean
    }
  }
  ready: () => void
  expand: () => void
  showAlert: (message: string) => void
}

declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp
    }
  }
}

interface User {
  id: string
  telegram_id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
}

interface AuthResponse {
  success: boolean
  user?: User
  error?: string
}

interface Family {
  id: string
  name: string
  currency_name: string
  currency_symbol: string
  invite_code: string
}

interface CreateFamilyResponse {
  success: boolean
  family?: Family
  error?: string
}

type AppMode = 'welcome' | 'create-family' | 'family-created' | 'join-family'

function App() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [user, setUser] = useState<User | null>(null)
  const [mode, setMode] = useState<AppMode>('welcome')
  
  const [familyName, setFamilyName] = useState('')
  const [currencyName, setCurrencyName] = useState('')
  const [currencySymbol, setCurrencySymbol] = useState('')
  const [createdFamily, setCreatedFamily] = useState<Family | null>(null)
  const [creating, setCreating] = useState(false)

  const apiUrl = import.meta.env.VITE_API_URL || 'https://family-wallet-api.maltsevstas21.workers.dev'

  useEffect(() => {
    const initTelegramAuth = async () => {
      try {
const tg = window.Telegram?.WebApp;
if (!tg) {
  console.warn('Telegram WebApp не найден - запускаем в браузере (MOCK режим).')
  setLoading(false)   // ← ВОТ ЭТА СТРОКА
  return;
}
        tg?.ready?.()
        tg?.expand?.()

        let initData = tg?.initData

        console.log('🔐 InitData:', initData ? 'есть' : 'ПУСТО')
        console.log('👤 User from initDataUnsafe:', tg?.initDataUnsafe?.user)

        // MOCK AUTH для тестирования (если initData пустой)
        if (!initData) {
          console.warn('⚠️ InitData пустой! Используем MOCK AUTH для тестирования')
          
          // Создаём mock initData из initDataUnsafe
          const mockUser = tg.initDataUnsafe?.user
          if (mockUser) {
            // Используем данные из initDataUnsafe напрямую
            const mockUserData: User = {
              id: `mock-${mockUser.id}`,
              telegram_id: mockUser.id,
              first_name: mockUser.first_name,
              last_name: mockUser.last_name,
              username: mockUser.username,
              language_code: mockUser.language_code || 'ru'
            }
            
            console.log('✅ MOCK USER:', mockUserData)
            setUser(mockUserData)
            setLoading(false)
            return
          }
          
setLoading(false); return;
        }

        // Нормальная авторизация
        console.log('🔐 Авторизация...', { apiUrl })

        const response = await fetch(`${apiUrl}/api/auth/verify`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-telegram-init-data': ((window as any).Telegram?.WebApp?.initData) || ''
          },
          body: JSON.stringify({}),
        })

        const data: AuthResponse = await response.json()

        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Ошибка авторизации')
        }

        setUser(data.user!)
        setLoading(false)

      } catch (err) {
        console.error('Auth error:', err)
        setError(err instanceof Error ? err.message : 'Неизвестная ошибка')
        setLoading(false)
      }
    }

    initTelegramAuth()
  }, [])

  const handleCreateFamily = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!familyName.trim() || !currencyName.trim() || !currencySymbol.trim()) {
      window.Telegram?.WebApp?.showAlert?.('Заполните все поля!') || alert('Заполните все поля!')
      return
    }

    setCreating(true)
    setError(null)

    try {
      const tg = window.Telegram?.WebApp
      let initData = tg?.initData || ''
      
      // Для MOCK режима используем пустой initData (backend включит dev mode)
      const isMockMode = user?.id?.startsWith('mock-')

      console.log('🏠 Создание семьи...', { 
        apiUrl, 
        endpoint: `${apiUrl}/api/families`,
        mockMode: isMockMode,
        hasInitData: !!initData,
        data: { familyName, currencyName, currencySymbol }
      })

      const response = await fetch(`${apiUrl}/api/families`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-telegram-init-data': (window as any).Telegram?.WebApp?.initData || ''
        },
        body: JSON.stringify({
          name: familyName.trim(),
          currency_name: currencyName.trim(),
          currency_symbol: currencySymbol.trim(),
        }),
      })

      console.log('📡 Response status:', response.status)

      const data: CreateFamilyResponse = await response.json()
      
      console.log('📦 Response data:', data)

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Ошибка создания семьи')
      }

      setCreatedFamily(data.family!)
      setMode('family-created')
      setCreating(false)

    } catch (err) {
      console.error('❌ Create family error:', err)
      const errorMessage = err instanceof Error ? err.message : 'Ошибка создания семьи'
      setError(errorMessage)
      setCreating(false)
      
      window.Telegram?.WebApp?.showAlert?.(errorMessage) || alert(errorMessage)
    }
  }

  const copyInviteCode = () => {
    if (createdFamily?.invite_code) {
      navigator.clipboard.writeText(createdFamily.invite_code)
        .then(() => {
          window.Telegram?.WebApp?.showAlert?.('✅ Код скопирован!') || alert('✅ Код скопирован!')
        })
        .catch(() => {
          window.Telegram?.WebApp?.showAlert?.('❌ Ошибка копирования') || alert('❌ Ошибка копирования')
        })
    }
  }

  if (loading) {
    return (
      <div className="app-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>🔐 Авторизация...</p>
        </div>
      </div>
    )
  }

  if (error && !user) {
    return (
      <div className="app-container">
        <div className="error">
          <h1>❌ Ошибка</h1>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="btn-retry">
            🔄 Попробовать снова
          </button>
        </div>
      </div>
    )
  }

  if (mode === 'welcome') {
    return (
      <div className="app-container">
        <div className="welcome">
          <h1>👋 Привет, {user?.first_name}!</h1>
          
          <div className="user-info">
            <p><strong>Telegram ID:</strong> {user?.telegram_id}</p>
            {user?.username && <p><strong>Username:</strong> @{user.username}</p>}
            {user?.language_code && <p><strong>Язык:</strong> {user.language_code}</p>}
            {user?.id?.startsWith('mock-') && (
              <p style={{color: '#ff8800'}}><strong>⚠️ Режим:</strong> MOCK (тест без initData)</p>
            )}
          </div>

          <div className="mode-selection">
            <h2>Выберите режим:</h2>
            
            <button className="btn-mode btn-parent" onClick={() => setMode('create-family')}>
              🏠 Создать семью
              <span className="mode-description">Я родитель</span>
            </button>

            <button className="btn-mode btn-child" onClick={() => setMode('join-family')}>
              👶 Присоединиться к семье
              <span className="mode-description">Я ребёнок</span>
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (mode === 'create-family') {
    return (
      <div className="app-container">
        <div className="form-container">
          <button className="btn-back" onClick={() => setMode('welcome')}>
            ← Назад
          </button>

          <h1>🏠 Создание семьи</h1>
          
          <form onSubmit={handleCreateFamily}>
            <div className="form-group">
              <label>Название семьи:</label>
              <input
                type="text"
                value={familyName}
                onChange={(e) => setFamilyName(e.target.value)}
                placeholder="Наша семья"
                maxLength={50}
                required
              />
            </div>

            <div className="form-group">
              <label>Валюта:</label>
              <input
                type="text"
                value={currencyName}
                onChange={(e) => setCurrencyName(e.target.value)}
                placeholder="Dragon Coins, Звёздочки, Бally"
                maxLength={30}
                required
              />
            </div>

            <div className="form-group">
              <label>Символ валюты:</label>
              <input
                type="text"
                value={currencySymbol}
                onChange={(e) => setCurrencySymbol(e.target.value)}
                placeholder="🐉, ⭐, 💎"
                maxLength={5}
                required
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            <button type="submit" className="btn-submit" disabled={creating}>
              {creating ? '⏳ Создаём...' : '✅ Создать семью'}
            </button>
          </form>
        </div>
      </div>
    )
  }

  if (mode === 'family-created' && createdFamily) {
    return (
      <div className="app-container">
        <div className="success-container">
          <h1>✅ Семья создана!</h1>
          
          <div className="family-info">
            <p><strong>Название:</strong> {createdFamily.name}</p>
            <p><strong>Валюта:</strong> {createdFamily.currency_name} {createdFamily.currency_symbol}</p>
          </div>

          <div className="invite-code-box">
            <h2>Invite Code:</h2>
            <div className="invite-code">{createdFamily.invite_code}</div>
            <p className="invite-hint">📋 Скопируй код и отправь ребёнку!</p>
            <button className="btn-copy" onClick={copyInviteCode}>
              📋 Копировать код
            </button>
          </div>

          <button className="btn-dashboard">
            ➡️ Перейти в Dashboard
          </button>
        </div>
      </div>
    )
  }

  if (mode === 'join-family') {
    return (
      <div className="app-container">
        <div className="form-container">
          <button className="btn-back" onClick={() => setMode('welcome')}>
            ← Назад
          </button>
          <h1>👶 Присоединение к семье</h1>
          <p style={{textAlign: 'center', color: '#888'}}>В разработке...</p>
        </div>
      </div>
    )
  }

  return null
}

export default App
