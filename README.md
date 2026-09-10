<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>HMF Book</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Poppins',sans-serif}
body{background:#dfe3e8;display:flex;justify-content:center;align-items:center;min-height:100vh}
.phone{width:100%;max-width:400px;height:100vh;max-height:850px;background:#fff;border-radius:35px;overflow:hidden;position:relative;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.screen{position:absolute;inset:0;display:none;flex-direction:column;overflow:hidden}
.screen.active{display:flex}
/* ===== SPLASH ===== */
.splash{background:linear-gradient(160deg,#00c980,#0a9e5c,#067a47);justify-content:center;align-items:center;position:relative}
.shape{position:absolute;opacity:.15}
.splash .logo{font-size:72px;font-weight:800;color:#fff;letter-spacing:-2px;text-shadow:0 5px 20px rgba(0,0,0,.2);z-index:2}
.splash .tag{color:#fff;font-size:26px;font-weight:600;z-index:2;margin-top:-8px}
.btn-get{margin-top:60px;background:#fff;color:#0a9e5c;border:none;padding:15px 55px;border-radius:50px;font-size:19px;font-weight:700;cursor:pointer;z-index:2;transition:.3s}
.btn-get:active{transform:scale(.95)}
/* ===== AUTH ===== */
.auth{background:linear-gradient(180deg,#0a9e5c 0%,#0fae66 40%,#fff 40%)}
.auth-head{height:38%;display:flex;justify-content:center;align-items:center}
.auth-head .logo{font-size:64px;font-weight:800;color:#fff;letter-spacing:-2px}
.sheet{background:#fff;border-radius:35px 35px 0 0;flex:1;padding:30px 28px;overflow-y:auto}
.sheet h2{font-size:28px;color:#1a1a1a;margin-bottom:20px}
.input-box{display:flex;align-items:center;gap:12px;border:2px solid #e3e6ea;border-radius:14px;padding:14px 16px;margin-bottom:14px}
.input-box input{border:none;outline:none;flex:1;font-size:15px;background:transparent}
.input-box svg{flex-shrink:0}
.btn-main{width:100%;background:linear-gradient(90deg,#0fae66,#00c980);color:#fff;border:none;padding:16px;border-radius:50px;font-size:18px;font-weight:700;cursor:pointer;margin-top:8px;transition:.3s}
.btn-main:active{transform:scale(.97)}
.divider{display:flex;align-items:center;gap:12px;color:#9aa1ab;font-size:14px;margin:22px 0 16px}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:#e3e6ea}
.socials{display:flex;justify-content:center;gap:22px}
.soc{width:52px;height:52px;border-radius:50%;display:flex;justify-content:center;align-items:center;cursor:pointer;border:none;color:#fff;font-weight:800;font-size:20px;transition:.3s}
.soc:active{transform:scale(.9)}
.soc.g{background:#ea4335}.soc.s{background:#fffc00;color:#fff}.soc.f{background:#1877f2}
.switch{text-align:center;margin-top:20px;font-size:14px;color:#666}
.switch a{color:#0a9e5c;font-weight:600;cursor:pointer;text-decoration:none}
/* ===== APP HEADER ===== */
.app-header{padding:16px 18px 10px;display:flex;justify-content:space-between;align-items:center;background:#fff}
.app-header .title{font-weight:800;font-size:22px;color:#1a1a1a}
.app-header .logo-sm{font-weight:800;font-size:24px;color:#0a9e5c;letter-spacing:-1px}
.icon-btn{background:#f2f4f6;border:none;width:38px;height:38px;border-radius:50%;cursor:pointer;display:flex;justify-content:center;align-items:center;margin-left:8px}
/* ===== CONTENT ===== */
.content{flex:1;overflow-y:auto;background:#fafafa;padding-bottom:80px}
.stories{display:flex;gap:14px;padding:12px 16px;overflow-x:auto;background:#fff}
.story{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:64px;cursor:pointer}
.story .ring{width:60px;height:60px;border-radius:50%;background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#bc1888);padding:3px}
.story .ring .in{width:100%;height:100%;border-radius:50%;border:2px solid #fff;display:flex;justify-content:center;align-items:center;font-weight:700;color:#fff;font-size:18px}
.story span{font-size:11px;color:#444}
.post{background:#fff;margin:10px 0;border-radius:4px}
.post-head{display:flex;align-items:center;gap:10px;padding:10px 14px}
.avatar{width:38px;height:38px;border-radius:50%;background:linear-gradient(45deg,#00c980,#056a45);display:flex;justify-content:center;align-items:center;color:#fff;font-weight:700;font-size:15px;flex-shrink:0}
.post-head b{font-size:14px}
.post-img{width:100%;height:280px;display:flex;justify-content:center;align-items:center;color:#fff;font-size:40px}
.post-actions{padding:10px 14px;font-size:20px;display:flex;gap:16px}
.post-body{padding:0 14px 12px;font-size:13px;color:#333}
/* ===== SHORTS ===== */
.shorts-wrap{flex:1;overflow-y:auto;scroll-snap-type:y mandatory}
.short{height:100%;scroll-snap-align:start;position:relative;display:flex;justify-content:center;align-items:center}
.short-info{position:absolute;bottom:90px;left:14px;color:#fff;z-index:3}
.short-info b{font-size:15px}.short-info p{font-size:13px;opacity:.9;margin-top:4px;max-width:230px}
.short-side{position:absolute;bottom:100px;right:12px;display:flex;flex-direction:column;gap:18px;align-items:center;z-index:3;color:#fff;font-size:11px}
.short-side .act{display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;font-size:24px}
/* ===== GAMES ===== */
.games-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:16px}
.game-card{background:#fff;border-radius:18px;padding:20px 14px;text-align:center;cursor:pointer;transition:.2s;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.game-card:active{transform:scale(.95)}
.game-card .gi{font-size:44px}
.game-card b{display:block;margin-top:8px;font-size:14px}
.game-card small{color:#0a9e5c;font-weight:600;font-size:11px}
/* ===== CHAT ===== */
.chat-item{display:flex;align-items:center;gap:12px;padding:12px 16px;cursor:pointer;background:#fff}
.chat-item:active{background:#f2f4f6}
.chat-item .ci{width:52px;height:52px;border-radius:50%;display:flex;justify-content:center;align-items:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0}
.chat-item div b{font-size:15px}.chat-item div p{font-size:13px;color:#888}
.chat-item .time{margin-left:auto;font-size:12px;color:#aaa}
/* ===== SEARCH ===== */
.search-bar{display:flex;align-items:center;gap:10px;background:#fff;border:2px solid #e3e6ea;margin:14px 16px;padding:12px 16px;border-radius:50px}
.search-bar input{border:none;outline:none;flex:1;font-size:15px}
.trends{padding:0 16px}
.trend{background:#fff;border-radius:14px;padding:14px;margin-bottom:10px;cursor:pointer}
.trend small{color:#888}.trend b{display:block;font-size:15px}.trend p{font-size:13px;color:#555;margin-top:3px}
/* ===== PROFILE ===== */
.pro-head{background:#fff;padding:24px 16px;text-align:center}
.pro-head .big{width:90px;height:90px;border-radius:50%;background:linear-gradient(45deg,#00c980,#056a45);margin:0 auto;display:flex;justify-content:center;align-items:center;color:#fff;font-size:34px;font-weight:800}
.pro-stats{display:flex;justify-content:center;gap:34px;margin-top:16px}
.pro-stats div{text-align:center}.pro-stats b{display:block;font-size:18px}.pro-stats span{font-size:12px;color:#888}
.btn-edit{margin-top:16px;background:#f2f4f6;border:none;padding:10px 30px;border-radius:10px;font-weight:600;cursor:pointer;font-size:14px}
.tabs{display:flex;background:#fff;border-top:1px solid #eee;border-bottom:1px solid #eee}
.tabs div{flex:1;text-align:center;padding:12px;font-size:20px;cursor:pointer;border-bottom:2px solid transparent}
.tabs div.on{border-color:#0a9e5c}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:2px;padding:2px}
.grid3 div{aspect-ratio:1;background:linear-gradient(135deg,#a8e6cf,#00c980);display:flex;justify-content:center;align-items:center;font-size:26px}
/* ===== SETTINGS ===== */
.set-group{background:#fff;border-radius:16px;margin:12px 14px;overflow:hidden}
.set-item{display:flex;align-items:center;gap:14px;padding:15px 16px;cursor:pointer;border-bottom:1px solid #f2f4f6}
.set-item:last-child{border:none}
.set-item:active{background:#f7f8f9}
.set-item .si{width:36px;height:36px;border-radius:10px;display:flex;justify-content:center;align-items:center;font-size:17px;flex-shrink:0}
.set-item div{flex:1}.set-item b{font-size:14.5px;font-weight:500;display:block}
.set-item small{font-size:12px;color:#999}
.set-item .arrow{color:#c5cbd2}
.toggle{width:44px;height:26px;background:#dfe3e8;border-radius:20px;position:relative;transition:.3s;flex-shrink:0}
.toggle.on{background:#0a9e5c}
.toggle::after{content:'';position:absolute;width:20px;height:20px;background:#fff;border-radius:50%;top:3px;left:3px;transition:.3s}
.toggle.on::after{left:21px}
/* ===== BOTTOM NAV ===== */
.bottom-nav{position:absolute;bottom:0;left:0;right:0;background:#fff;display:flex;border-top:1px solid #eee;padding:8px 0 12px;z-index:10}
.bottom-nav div{flex:1;text-align:center;cursor:pointer;font-size:22px;opacity:.45;transition:.2s}
.bottom-nav div.on{opacity:1}
.bottom-nav div .center-btn{width:48px;height:48px;background:linear-gradient(90deg,#0fae66,#00c980);border-radius:14px;margin:-4px auto 0;display:flex;justify-content:center;align-items:center;color:#fff;font-size:24px}
::-webkit-scrollbar{display:none}
</style>
</head>
<body>
<div class="phone">

<!-- SPLASH -->
<div class="screen splash active" id="scr-splash">
  <svg class="shape" style="top:40px;left:-30px" width="200" height="200"><polygon points="30,10 90,180 10,90" fill="none" stroke="#fff" stroke-width="2"/></svg>
  <svg class="shape" style="top:120px;right:-20px" width="180" height="180"><polygon points="90,10 170,170 10,170" fill="none" stroke="#fff" stroke-width="2"/></svg>
  <svg class="shape" style="bottom:120px;left:30px" width="140" height="140"><polygon points="70,10 130,130 10,130" fill="none" stroke="#fff" stroke-width="2"/></svg>
  <svg class="shape" style="bottom:200px;right:40px" width="120" height="120"><polygon points="60,5 115,115 5,115" fill="none" stroke="#fff" stroke-width="2"/></svg>
  <div class="logo">HMF</div>
  <div class="tag">HMF book</div>
  <button class="btn-get" onclick="show('scr-signup')">Get Started</button>
</div>

<!-- SIGNUP -->
<div class="screen auth" id="scr-signup">
  <div class="auth-head"><div class="logo">HMF</div></div>
  <div class="sheet">
    <h2>Create Account</h2>
    <div class="input-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9aa1ab" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg><input id="su-user" placeholder="Username"></div>
    <div class="input-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9aa1ab" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg><input id="su-email" type="email" placeholder="Email"></div>
    <div class="input-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9aa1ab" stroke-width="2"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/></svg><input id="su-pass" type="password" placeholder="Password"><span onclick="togglePass('su-pass',this)" style="cursor:pointer">👁</span></div>
    <button class="btn-main" onclick="signup()">Sign Up</button>
    <div class="divider">Or continue with</div>
    <div class="socials">
      <button class="soc g" onclick="enterApp('Google')">G</button>
      <button class="soc s" onclick="enterApp('Snapchat')">👻</button>
      <button class="soc f" onclick="enterApp('Facebook')">f</button>
    </div>
    <p class="switch">Already have an account? <a onclick="show('scr-login')">Log in</a></p>
  </div>
</div>

<!-- LOGIN -->
<div class="screen auth" id="scr-login">
  <div class="auth-head"><div class="logo">HMF</div></div>
  <div class="sheet">
    <h2>Welcome Back</h2>
    <div class="input-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9aa1ab" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg><input type="email" placeholder="Email or Username"></div>
    <div class="input-box"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9aa1ab" stroke-width="2"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 018 0v3"/></svg><input type="password" placeholder="Password"><span onclick="togglePass(this.previousElementSibling,this)" style="cursor:pointer">👁</span></div>
    <button class="btn-main" onclick="enterApp()">Log In</button>
    <div class="divider">Or continue with</div>
    <div class="socials">
      <button class="soc g" onclick="enterApp('Google')">G</button>
      <button class="soc s" onclick="enterApp('Snapchat')">👻</button>
      <button class="soc f" onclick="enterApp('Facebook')">f</button>
    </div>
    <p class="switch">Don't have an account? <a onclick="show('scr-signup')">Sign up</a></p>
  </div>
</div>

<!-- HOME -->
<div class="screen" id="scr-home">
  <div class="app-header"><div class="logo-sm">HMF book</div><div><button class="icon-btn" onclick="show('scr-search')">🔍</button><button class="icon-btn" onclick="show('scr-settings')">⚙️</button></div></div>
  <div class="content">
    <div class="stories">
      <div class="story"><div class="ring"><div class="in" style="background:#0a9e5c">+</div></div><span>Your story</span></div>
      <div class="story"><div class="ring"><div class="in" style="background:#e1306c">A</div></div><span>ali_khan</span></div>
      <div class="story"><div class="ring"><div class="in" style="background:#f77737">S</div></div><span>sara99</span></div>
      <div class="story"><div class="ring"><div class="in" style="background:#833ab4">U</div></div><span>usman</span></div>
      <div class="story"><div class="ring"><div class="in" style="background:#fdcb6e">Z</div></div><span>zain_12</span></div>
    </div>
    <div class="post">
      <div class="post-head"><div class="avatar">A</div><div><b>ali_khan</b><br><small style="color:#999;font-size:12px">Lahore</small></div><span style="margin-left:auto">⋯</span></div>
      <div class="post-img" style="background:linear-gradient(135deg,#00c980,#0a5c3c)">🌄</div>
      <div class="post-actions"><span onclick="this.style.color='red'">❤️</span><span>💬</span><span>📤</span></div>
      <div class="post-body"><b>1,240 likes</b><br>HMF book pehla post! 🎉 #hmfbook</div>
    </div>
    <div class="post">
      <div class="post-head"><div class="avatar" style="background:linear-gradient(45deg,#f09433,#dc2743)">S</div><div><b>sara99</b><br><small style="color:#999;font-size:12px">Karachi</small></div><span style="margin-left:auto">⋯</span></div>
      <div class="post-img" style="background:linear-gradient(135deg,#667eea,#764ba2)">🌇</div>
      <div class="post-actions"><span>❤️</span><span>💬</span><span>📤</span></div>
      <div class="post-body"><b>856 likes</b><br>Beautiful evening ✨</div>
    </div>
  </div>
</div>

<!-- SHORTS -->
<div class="screen" id="scr-shorts">
  <div class="app-header"><div class="title">Shorts</div><button class="icon-btn" onclick="show('scr-settings')">⚙️</button></div>
  <div class="shorts-wrap" id="shortsWrap"></div>
</div>

<!-- GAMES -->
<div class="screen" id="scr-games">
  <div class="app-header"><div class="title">🎮 Games</div><button class="icon-btn" onclick="show('scr-settings')">⚙️</button></div>
  <div class="content"><div class="games-grid">
    <div class="game-card" onclick="playGame('Snake')"><div class="gi">🐍</div><b>Snake</b><small>PLAY NOW</small></div>
    <div class="game-card" onclick="playGame('Memory')"><div class="gi">🧠</div><b>Memory</b><small>PLAY NOW</small></div>
    <div class="game-card" onclick="playGame('Tic Tac Toe')"><div class="gi">⭕</div><b>Tic Tac Toe</b><small>PLAY NOW</small></div>
    <div class="game-card" onclick="playGame('2048')"><div class="gi">🔢</div><b>2048</b><small>PLAY NOW</small></div>
    <div class="game-card" onclick="playGame('Quiz')"><div class="gi">❓</div><b>Quiz</b><small>PLAY NOW</small></div>
    <div class="game-card" onclick="playGame('Racing')"><div class="gi">🏎️</div><b>Racing</b><small>PLAY NOW</small></div>
  </div></div>
</div>

<!-- CHAT -->
<div class="screen" id="scr-chat">
  <div class="app-header"><div class="title">👻 Chats</div><button class="icon-btn" onclick="show('scr-settings')">⚙️</button></div>
  <div class="content">
    <div class="chat-item"><div class="ci" style="background:#fffc00;color:#333">👻</div><div><b>ali_khan</b><p><i style="color:#f43f5e;font-weight:700">❤ New Snap</i></p></div><span class="time">2m</span></div>
    <div class="chat-item"><div class="ci" style="background:#833ab4">U</div><div><b>usman</b><p>Delivered</p></div><span class="time">10m</span></div>
    <div class="chat-item"><div class="ci" style="background:#f77737">S</div><div><b>sara99</b><p><i style="color:#0a9e5c;font-weight:700">Opened</i></p></div><span class="time">1h</span></div>
    <div class="chat-item"><div class="ci" style="background:#0a9e5c">G</div><div><b>HMF Group</b><p>Ali: Salam sab ko! 👋</p></div><span class="time">3h</span></div>
    <div class="chat-item"><div class="ci" style="background:#e1306c">Z</div><div><b>zain_12</b><p><i style="color:#f43f5e;font-weight:700">🔥 Streak</i></p></div><span class="time">5h</span></div>
  </div>
</div>

<!-- SEARCH -->
<div class="screen" id="scr-search">
  <div class="app-header"><div class="title">Search</div></div>
  <div class="search-bar">🔍<input placeholder="Google, YouTube search karein..."></div>
  <div class="content trends">
    <div class="trend" onclick="openLink('https://youtube.com')"><small>📺 YouTube</small><b>Trending Videos</b><p>Watch latest videos on YouTube</p></div>
    <div class="trend" onclick="openLink('https://google.com')"><small>🔎 Google</small><b>Search the Web</b><p>Search anything on Google</p></div>
    <div class="trend" onclick="openLink('https://tiktok.com')"><small>🎵 TikTok</small><b>Trending Now</b><p>Viral TikTok videos</p></div>
    <div class="trend" onclick="openLink('https://instagram.com')"><small>📸 Instagram</small><b>Explore</b><p>Photos & reels from Instagram</p></div>
    <div class="trend" onclick="openLink('https://snapchat.com')"><small>👻 Snapchat</small><b>Snap Map</b><p>See what's happening nearby</p></div>
  </div>
</div>

<!-- PROFILE -->
<div class="screen" id="scr-profile">
  <div class="app-header"><div class="title">My Profile</div><div><button class="icon-btn" onclick="show('scr-settings')">☰</button></div></div>
  <div class="pro-head">
    <div class="big" id="proAvatar">H</div>
    <h3 style="margin-top:10px" id="proName">@hmf_user</h3>
    <p style="font-size:13px;color:#888">HMF Book 🚀 | All-in-one app</p>
    <div class="pro-stats">
      <div><b>24</b><span>Posts</span></div>
      <div><b>1.2K</b><span>Followers</span></div>
      <div><b>380</b><span>Following</span></div>
    </div>
    <button class="btn-edit" onclick="show('scr-settings')">Edit Profile</button>
  </div>
  <div class="tabs"><div class="on">🖼️</div><div>🎬</div><div>🏷️</div></div>
  <div class="content" style="padding-bottom:90px"><div class="grid3">
    <div>🌄</div><div>🌇</div><div>🌊</div><div>🏔️</div><div>🌆</div><div>🌺</div><div>🎮</div><div>📸</div><div>✨</div>
  </div></div>
</div>

<!-- SETTINGS (Instagram Style) -->
<div class="screen" id="scr-settings">
  <div class="app-header"><div class="title">Settings & Privacy</div></div>
  <div class="content" style="padding-bottom:30px">
    <div class="set-item" style="cursor:default"><div class="avatar">H</div><div><b id="setName">@hmf_user</b><small>HMF Book account</small></div></div>

    <div class="set-group">
      <div class="set-item" onclick="alert('Account Center')"><div class="si" style="background:#e8f7f0">👤</div><div><b>Account Center</b><small>Password, Personal details</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('Saved posts')"><div class="si" style="background:#fff5e6">🔖</div><div><b>Saved</b><small>Manage saved posts</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('Archive')"><div class="si" style="background:#f0efff">🗄️</div><div><b>Archive</b><small>Stories & posts archive</small></div><span class="arrow">›</span></div>
    </div>

    <div class="set-group">
      <div class="set-item" onclick="alert('Notifications')"><div class="si" style="background:#ffe8ec">🔔</div><div><b>Notifications</b><small>Likes, comments, follows</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="toggleT(this)"><div class="si" style="background:#e8f2ff">🌙</div><div><b>Dark Mode</b><small>Change app theme</small></div><div class="toggle"></div></div>
      <div class="set-item" onclick="toggleT(this)"><div class="si" style="background:#e8f7f0">⏰</div><div><b>Your Activity</b><small>Time spent reminders</small></div><div class="toggle on"></div></div>
    </div>

    <div class="set-group">
      <div class="set-item" onclick="alert('Privacy')"><div class="si" style="background:#e8f7f0">🔒</div><div><b>Privacy</b><small>Private account, comments</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('Security')"><div class="si" style="background:#fff5e6">🛡️</div><div><b>Security</b><small>Two-factor authentication</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('Blocked accounts')"><div class="si" style="background:#ffe8ec">🚫</div><div><b>Blocked</b><small>Blocked accounts list</small></div><span class="arrow">›</span></div>
    </div>

    <div class="set-group">
      <div class="set-item" onclick="alert('Language: English / اردو')"><div class="si" style="background:#f0efff">🌐</div><div><b>Language</b><small>English (US)</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('Data Saver')"><div class="si" style="background:#e8f2ff">📶</div><div><b>Data Usage & Media Quality</b><small>Data saver mode</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('Linked apps: YouTube, TikTok, Google, Snapchat, Instagram, Games')"><div class="si" style="background:#e8f7f0">🔗</div><div><b>Linked Apps</b><small>Connect your other apps</small></div><span class="arrow">›</span></div>
    </div>

    <div class="set-group">
      <div class="set-item" onclick="alert('Help Center')"><div class="si" style="background:#fff5e6">❓</div><div><b>Help</b><small>Report a problem</small></div><span class="arrow">›</span></div>
      <div class="set-item" onclick="alert('About HMF Book v1.0')"><div class="si" style="background:#f0efff">ℹ️</div><div><b>About</b><small>HMF Book v1.0</small></div><span class="arrow">›</span></div>
    </div>

    <div class="set-group" style="text-align:center;padding:8px 0">
      <div class="set-item" style="justify-content:center;color:#e1306c;font-weight:600" onclick="logout()">Log Out</div>
    </div>
  </div>
</div>

<!-- BOTTOM NAV -->
<div class="bottom-nav" id="bottomNav" style="display:none">
  <div class="on" onclick="goTab(this,'scr-home')">🏠</div>
  <div onclick="goTab(this,'scr-shorts')">🎬</div>
  <div onclick="goTab(this,'scr-games')"><div class="center-btn">🎮</div></div>
  <div onclick="goTab(this,'scr-chat')">👻</div>
  <div onclick="goTab(this,'scr-profile')">👤</div>
</div>

</div>
<script>
function show(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active');}
function togglePass(id,el){id.type=id.type==='password'?'text':'password';}
function signup(){const u=document.getElementById('su-user').value;if(!u){alert('Username likhein!');return;}enterApp();}
function enterApp(via){if(via)alert('Signed in with '+via+'!');document.getElementById('proName').textContent='@'+(document.getElementById('su-user').value||'hmf_user');document.getElementById('setName').textContent='@'+(document.getElementById('su-user').value||'hmf_user');document.getElementById('proAvatar').textContent=(document.getElementById('su-user').value||'H')[0].toUpperCase();show('scr-home');document.getElementById('bottomNav').style.display='flex';}
function logout(){document.getElementById('bottomNav').style.display='none';show('scr-login');}
function goTab(el,id){document.querySelectorAll('.bottom-nav div').forEach(d=>d.classList.remove('on'));el.classList.add('on');show(id);}
function toggleT(el){el.querySelector('.toggle').classList.toggle('on');}
function openLink(url){window.open(url,'_blank');}
function playGame(g){alert('🎮 '+g+' loading... Coming soon!');}
/* Shorts content */
const shorts=[{g:'linear-gradient(135deg,#ff6b6b,#ee5a24)',u:'ali_khan',d:'Viral dance 🔥 #trending',l:'12.5K'},{g:'linear-gradient(135deg,#0abde3,#341f97)',u:'sara99',d:'Nature vibes 🌊',l:'8.2K'},{g:'linear-gradient(135deg,#00c980,#0a5c3c)',u:'usman',d:'HMF Book shorts! 🚀',l:'21K'},{g:'linear-gradient(135deg,#f368e0,#a55eea)',u:'zain_12',d:'Funny moment 😂',l:'15K'}];
document.getElementById('shortsWrap').innerHTML=shorts.map(s=>`<div class="short" style="background:${s.g}"><div class="short-info"><b>@${s.u}</b><p>${s.d}</p></div><div class="short-side"><div class="act">❤️<span>${s.l}</span></div><div class="act">💬<span>320</span></div><div class="act">📤<span>Share</span></div></div><div style="font-size:70px;opacity:.5">▶️</div></div>`).join('');
</script>
</body>
</html>
