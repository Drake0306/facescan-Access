const { app, BrowserWindow } = require('electron')

console.log('app type:', typeof app)
console.log('BrowserWindow type:', typeof BrowserWindow)

app.whenReady().then(() => {
  console.log('Electron app is ready!')
  app.quit()
})
