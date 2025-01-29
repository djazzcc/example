'use strict'

const THEMES = ['auto', 'light', 'dark']
const ICONS = {
    'auto': 'bi-circle-half',
    'light': 'bi-sun-fill',
    'dark': 'bi-moon-stars-fill'
}

const getStoredTheme = () => localStorage.getItem('theme') || 'auto'
const setStoredTheme = theme => localStorage.setItem('theme', theme)

const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'auto') {
        return storedTheme
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const setTheme = theme => {
    if (theme === 'auto') {
        document.documentElement.setAttribute('data-bs-theme', 
            window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
        )
    } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
    }
}

const showActiveTheme = (theme) => {
    const themeSwitcher = document.querySelector('#bd-theme')
    const themeIcon = document.querySelector('.theme-icon-active')
    
    if (!themeSwitcher || !themeIcon) return

    themeIcon.className = `bi ${ICONS[theme]} theme-icon-active`
    
    const themeSwitcherText = document.querySelector('#bd-theme-text')
    if (themeSwitcherText) {
        themeSwitcherText.textContent = `${theme.charAt(0).toUpperCase() + theme.slice(1)} mode`
    }
}

const cycleTheme = () => {
    const currentTheme = getStoredTheme()
    const currentIndex = THEMES.indexOf(currentTheme)
    const nextIndex = (currentIndex + 1) % THEMES.length
    const nextTheme = THEMES[nextIndex]
    
    setStoredTheme(nextTheme)
    setTheme(nextTheme)
    showActiveTheme(nextTheme)
}

const initializeTheme = () => {
    // Set theme immediately
    const initialTheme = getStoredTheme()
    setTheme(initialTheme)
    showActiveTheme(initialTheme)

    // Wait for DOM to be ready before attaching handlers
    if (document.readyState === 'loading') {
        window.addEventListener('DOMContentLoaded', attachThemeHandlers)
    } else {
        attachThemeHandlers()
    }
}

const attachThemeHandlers = () => {
    // Handle system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        const currentTheme = getStoredTheme()
        if (currentTheme === 'auto') {
            setTheme('auto')
        }
    })

    // Handle theme toggle button
    const themeToggle = document.querySelector('#bd-theme')
    if (themeToggle) {
        themeToggle.addEventListener('click', cycleTheme)
    }
}

export { initializeTheme } 