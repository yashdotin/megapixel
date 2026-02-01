function toggleTheme() {
  const html = document.documentElement
  if (html.classList.contains('dark')) {
    html.classList.remove('dark')
    localStorage.theme = 'light'
  } else {
    html.classList.add('dark')
    localStorage.theme = 'dark'
  }
}
