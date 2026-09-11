import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HMF Book", page_icon="🟢", layout="wide")

st.markdown("<style>#MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}</style>", unsafe_allow_html=True)

APP_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HMF Book</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Arial,sans-serif}
body{background:#fff;display:flex;justify-content:center}
.phone{width:100%;max-width:430px;min-height:100vh;background:#fff;position:relative}
.screen{display:none;min-height:100vh;flex-direction:column}
.screen.active{display:flex}
#splash{background:linear-gradient(140deg,#00e08a,#00b45a 45%,#009e4f);justify-content:center;align-items:center;text-align:center}
.hmf-logo{font-size:78px;font-weight:900;color:#fff;letter-spacing:2px;font-style:italic}
.hmf-sub{font-size:26px;color:#fff;font-weight:600;margin-top:6px}
.get-started{margin-top:70px;padding:15px 60px;border:none;border-radius:999px;background:#fff;color:#009e4f;font-size:19px;font-weight:800;cursor:pointer}
.auth-top{background:linear-gradient(140deg,#00e08a,#00b45a 45%,#009e4f);padding:60px 30px 90px;text-align:center}
.auth-top .hmf-logo{font-size:56px}
.auth-card{background:#fff;border-radius:28px 28px 0 0;margin-top:-45px;padding:30px 24px 40px;flex:1}
.auth-card h1{font-size:30px;color:#222;margin-bottom:22px}
.input-box{display:flex;align-items:center;gap:10px;border:1.5px solid #dfe3e8;border-radius:14px;padding:13px 14px;margin-bottom:14px}
.input-box input{border:none;outline:none;flex:1;font-size:15px}
.eye{cursor:pointer;background:none;border:none;font-size:16px}
.btn{width:100%;padding:14px;border:none;border-radius:999px;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:17px;font-weight:800;cursor:pointer;margin-top:8px}
.divider{display:flex;align-items:center;gap:12px;color:#8a9299;font-size:14px;margin:22px 0 16px}
.divider:before,.divider:after{content:"";flex:1;height:1px;background:#e3e7eb}
.social-row{display:flex;justify-content:center;gap:26px}
.social{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;cursor:pointer;border:none;color:#fff}
.g-g{background:#fff;border:2px solid #eee;color:#ea4335}
.g-s{background:#fffc00}
.g-f{background:#1877f2}
.switch-auth{text-align:center;margin-top:24px;font-size:14px;color:#5b6167}
.switch-auth a{color:#009e4f;font-weight:700;cursor:pointer}
#app{height:100vh}
.app-header{background:linear-gradient(140deg,#00e08a,#009e4f);color:#fff;padding:14px 18px;display:flex;align-items:center;justify-content:space-between}
.brand{font-size:22px;font-weight:900;font-style:italic}
.content{flex:1;overflow-y:auto;background:#f7f8fa}
.page{display:none}
.page.active{display:block}
.bottom-nav{display:flex;background:#fff;border-top:1px solid #eceff2}
.nav-btn{flex:1;padding:10px 0 12px;font-size:20px;background:none;border:none;cursor:pointer;filter:grayscale(1);opacity:.55}
.nav-btn.active{filter:none;opacity:1}
.nav-btn span{display:block;font-size:10px;color:#5b6167;margin-top:2px}
.stories{display:flex;gap:14px;overflow-x:auto;padding:14px;background:#fff;border-bottom:1px solid #eceff2}
.story{text-align:center;font-size:11px;color:#333;min-width:60px}
.story-av{width:56px;height:56px;border-radius:50%;border:2.5px solid #00d67e;padding:2.5px;display:flex;align-items:center;justify-content:center;background:#fff;margin:0 auto}
.story-av div{width:100%;height:100%;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:20px}
.av1{background:linear-gradient(135deg,#f9ce34,#ee2a7b)}
.av2{background:linear-gradient(135deg,#667eea,#764ba2)}
.av3{background:linear-gradient(135deg,#11998e,#38ef7d)}
.av4{background:linear-gradient(135deg,#fc4a1a,#f7b733)}
.my-story .story-av{border-style:dashed;color:#009e4f;font-size:26px;font-weight:800}
.post{background:#fff;margin:12px;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.post-head{display:flex;align-items:center;gap:10px;padding:10px 12px}
.mini-av{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800}
.muted{color:#8a9299;font-size:12px}
.dots{margin-left:auto;font-size:20px;color:#5b6167;cursor:pointer}
.post-img{height:230px;display:flex;align-items:center;justify-content:center;font-size:74px;position:relative;cursor:pointer}
.p1{background:linear-gradient(135deg,#89f7fe,#66a6ff)}
.p2{background:linear-gradient(135deg,#fddb92,#d1fdff)}
.p3{background:linear-gradient(135deg,#a18cd1,#fbc2eb)}
.big-heart{position:absolute;font-size:90px;animation:pop .8s ease}
@keyframes pop{0%{transform:scale(0);opacity:0}40%{transform:scale(1.2);opacity:1}100%{transform:scale(1);opacity:0}}
.post-actions{display:flex;gap:16px;padding:10px 12px;font-size:20px}
.icon-btn{background:none;border:none;font-size:20px;cursor:pointer}
.save-btn{margin-left:auto}
.caption{padding:0 12px 12px;font-size:14px}
.reel{height:55vh;min-height:360px;border-radius:18px;margin:12px;position:relative;display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.r1{background:linear-gradient(160deg,#ff512f,#dd2476)}
.r2{background:linear-gradient(160deg,#11998e,#38ef7d)}
.r3{background:linear-gradient(160deg,#41295a,#2f0743)}
.reel-emoji{position:absolute;top:20%;left:50%;transform:translateX(-50%);font-size:80px}
.reel-info{padding:16px;width:100%}
.reel-info h3{font-size:16px;margin-bottom:4px}
.reel-side{position:absolute;right:12px;bottom:20px;display:flex;flex-direction:column;gap:18px}
.reel-side .icon-btn{color:#fff;font-size:24px}
.search-wrap{padding:20px}
.google-logo{text-align:center;font-size:40px;font-weight:800;margin:14px 0 20px}
.l-red{color:#ea4335}.l-blue{color:#4285f4}.l-green{color:#34a853}.l-yellow{color:#fbbc05}
.search-bar{display:flex;align-items:center;gap:10px;background:#fff;border:1.5px solid #dfe3e8;border-radius:999px;padding:13px 18px}
.search-bar input{border:none;outline:none;flex:1;font-size:15px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.chip{background:#fff;border:1px solid #dfe3e8;border-radius:999px;padding:8px 14px;font-size:13px;cursor:pointer}
.link-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px}
.link-card{background:#fff;border-radius:16px;padding:16px 6px;text-align:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.link-card div{width:44px;height:44px;border-radius:50%;margin:0 auto 8px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:900}
.link-card p{font-size:12px;color:#333}
.game-wrap{padding:20px;text-align:center}
#gameStatus{font-size:17px;font-weight:700;margin:12px 0;color:#009e4f}
#ttt{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:300px;margin:0 auto}
.cell{aspect-ratio:1;background:#fff;border:2px solid #e3e7eb;border-radius:12px;font-size:36px;font-weight:800;color:#009e4f;display:flex;align-items:center;justify-content:center;cursor:pointer}
.btn-outline{margin-top:16px;padding:10px 30px;border:2px solid #009e4f;border-radius:999px;background:#fff;color:#009e4f;font-weight:700;cursor:pointer}
.coming{margin-top:26px;background:#fff;border-radius:16px;padding:22px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.profile-head{background:#fff;padding:24px 16px;text-align:center;border-bottom:1px solid #eceff2}
.big-av{width:86px;height:86px;border-radius:50%;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:36px;font-weight:800;display:flex;align-items:center;justify-content:center;margin:0 auto 10px}
.stats{display:flex;justify-content:center;gap:34px;margin:16px 0}
.stats b{display:block;font-size:18px}
.stats span{font-size:12px;color:#8a9299}
.pill-row{display:flex;gap:10px;justify-content:center}
.pill{padding:9px 22px;border-radius:999px;border:1.5px solid #dfe3e8;background:#fff;font-weight:700;cursor:pointer;font-size:14px}
.pill.green{background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;border:none}
.grid6{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px}
.gtile{aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-size:38px;color:#fff}
#settingsScreen{position:absolute;top:0;left:0;right:0;bottom:0;background:#f3f4f6;overflow-y:auto;display:none;z-index:50}
#settingsScreen.active{display:block}
.set-head{background:linear-gradient(140deg,#00e08a,#009e4f);color:#fff;padding:16px 18px 20px;display:flex;align-items:center;gap:14px}
.back-btn{background:none;border:none;color:#fff;font-size:22px;cursor:pointer}
.set-summary{background:#fff;margin:14px;border-radius:16px;padding:16px;display:flex;gap:14px;align-items:center}
.set-group{background:#fff;margin:14px;border-radius:16px;overflow:hidden}
.set-group h4{padding:12px 16px 4px;color:#009e4f;font-size:13px;text-transform:uppercase}
.set-row{display:flex;align-items:center;gap:12px;padding:14px 16px;border-top:1px solid #f0f2f4;cursor:pointer;font-size:15px}
.set-row .chev{margin-left:auto;color:#b3b9bf}
.set-row.danger{color:#ed4956}
#toast{position:fixed;bottom:95px;left:50%;transform:translateX(-50%);background:#222;color:#fff;padding:11px 20px;border-radius:999px;font-size:14px;opacity:0;pointer-events:none;transition:.3s;z-index:100}
#toast.show{opacity:1}
</style>
</head>
<body>
<div class="phone">
<div id="splash" class="screen active">
  <div><div class="hmf-logo">HMF</div><div class="hmf-sub">HMF book</div></div>
  <button class="get-started" onclick="showScreen('auth')">Get Started</button>
</div>
<div id="auth" class="screen">
  <div class="auth-top"><div class="hmf-logo">HMF</div></div>
  <div class="auth-card">
    <h1>Create Account</h1>
    <div class="input-box">👤<input id="suUser" type="text" placeholder="Username"></div>
    <div class="input-box">✉️<input id="suEmail" type="email" placeholder="Email"></div>
    <div class="input-box">🔒<input id="suPass" type="password" placeholder="Password"><button class="eye" onclick="togglePass('suPass',this)">👁️</button></div>
    <button class="btn" onclick="signup()">Sign Up</button>
    <div class="divider">Or continue with</div>
    <div class="social-row">
      <button class="social g-g" onclick="socialLogin('Google')">G</button>
      <button class="social g-s" onclick="socialLogin('Snapchat')">👻</button>
      <button class="social g-f" onclick="socialLogin('Facebook')">f</button>
    </div>
    <p class="switch-auth">Already have an account? <a onclick="showScreen('login')">Log in</a></p>
  </div>
</div>
<div id="login" class="screen">
  <div class="auth-top"><div class="hmf-logo">HMF</div></div>
  <div class="auth-card">
    <h1>Welcome Back</h1>
    <div class="input-box">✉️<input id="liEmail" type="email" placeholder="Email"></div>
    <div class="input-box">🔒<input id="liPass" type="password" placeholder="Password"><button class="eye" onclick="togglePass('liPass',this)">👁️</button></div>
    <button class="btn" onclick="login()">Log In</button>
    <p class="switch-auth">New here? <a onclick="showScreen('auth')">Create Account</a></p>
  </div>
</div>
<div id="app" class="screen">
  <div class="app-header">
    <div class="brand">HMF book</div>
    <div style="display:flex;gap:14px;font-size:20px">
      <span onclick="showToast('Messages')" style="cursor:pointer">📩</span>
      <span onclick="openSettings()" style="cursor:pointer">⚙️</span>
    </div>
  </div>
  <div class="content">
    <div id="pageHome" class="page active">
      <div class="stories">
        <div class="story my-story"><div class="story-av"><div id="myStoryAvatar">+</div></div>Your story</div>
        <div class="story"><div class="story-av"><div class="av1">A</div></div>Ahmed</div>
        <div class="story"><div class="story-av"><div class="av2">S</div></div>Sara</div>
        <div class="story"><div class="story-av"><div class="av3">B</div></div>Bilal</div>
        <div class="story"><div class="story-av"><div class="av4">Z</div></div>Zara</div>
      </div>
      <div class="post">
        <div class="post-head"><div class="mini-av av1">A</div><div><b>Ahmed</b><br><span class="muted">Hunza Valley</span></div><span class="dots">⋯</span></div>
        <div class="post-img p1" onclick="doubleLike(this)">🏔️</div>
        <div class="post-actions"><button class="icon-btn like-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="showToast('Shared!')">✈️</button><button class="icon-btn save-btn" onclick="showToast('Saved')">🔖</button></div>
        <div class="caption"><b>Ahmed</b> Beautiful Pakistan 🇵🇰</div>
      </div>
      <div class="post">
        <div class="post-head"><div class="mini-av av2">S</div><div><b>Sara</b><br><span class="muted">Original audio</span></div><span class="dots">⋯</span></div>
        <div class="post-img p2" onclick="doubleLike(this)">🎵</div>
        <div class="post-actions"><button class="icon-btn like-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="showToast('Shared!')">✈️</button><button class="icon-btn save-btn" onclick="showToast('Saved')">🔖</button></div>
        <div class="caption"><b>Sara</b> New reel trend! 🔥</div>
      </div>
      <div class="post">
        <div class="post-head"><div class="mini-av av3">B</div><div><b>Bilal</b><br><span class="muted">Gaming</span></div><span class="dots">⋯</span></div>
        <div class="post-img p3" onclick="doubleLike(this)">🎮</div>
        <div class="post-actions"><button class="icon-btn like-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="showToast('Shared!')">✈️</button><button class="icon-btn save-btn" onclick="showToast('Saved')">🔖</button></div>
        <div class="caption"><b>Bilal</b> Game night on HMF 🕹️</div>
      </div>
    </div>
    <div id="pageReels" class="page">
      <div class="reel r1">
        <div class="reel-emoji">💃</div>
        <div class="reel-side"><button class="icon-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="showToast('Shared!')">✈️</button></div>
        <div class="reel-info"><h3>@trendstar</h3><p>TikTok style trend 🎶</p></div>
      </div>
      <div class="reel r2">
        <div class="reel-emoji">🐱</div>
        <div class="reel-side"><button class="icon-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="showToast('Shared!')">✈️</button></div>
        <div class="reel-info"><h3>@funny.pets</h3><p>Cat boss 😹</p></div>
      </div>
      <div class="reel r3">
        <div class="reel-emoji">⚽</div>
        <div class="reel-side"><button class="icon-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="showToast('Shared!')">✈️</button></div>
        <div class="reel-info"><h3>@sports.hub</h3><p>Goal of the year! 🥅</p></div>
      </div>
    </div>
    <div id="pageSearch" class="page">
      <div class="search-wrap">
        <div class="google-logo"><span class="l-blue">H</span><span class="l-red">M</span><span class="l-yellow">F</span><span class="l-green"> Search</span></div>
        <div class="search-bar">🔍<input id="searchInput" type="text" placeholder="Search Google or type a URL" onkeydown="if(event.key==='Enter')doSearch()"></div>
        <div class="chips">
          <span class="chip" onclick="setQuery('TikTok trending')">TikTok trending</span>
          <span class="chip" onclick="setQuery('YouTube shorts')">YouTube shorts</span>
          <span class="chip" onclick="setQuery('Instagram reels')">Instagram reels</span>
          <span class="chip" onclick="setQuery('Free online games')">Free online games</span>
        </div>
        <div class="link-grid">
          <div class="link-card" onclick="openSite('https://www.google.com')"><div style="background:#fff;border:2px solid #eee;color:#4285f4">G</div><p>Google</p></div>
          <div class="link-card" onclick="openSite('https://www.youtube.com')"><div style="background:#ff0000">▶</div><p>YouTube</p></div>
          <div class="link-card" onclick="openSite('https://www.tiktok.com')"><div style="background:#010101">🎵</div><p>TikTok</p></div>
          <div class="link-card" onclick="openSite('https://www.instagram.com')"><div style="background:linear-gradient(135deg,#f9ce34,#ee2a7b)">📷</div><p>Instagram</p></div>
          <div class="link-card" onclick="openSite('https://www.snapchat.com')"><div style="background:#fffc00">👻</div><p>Snapchat</p></div>
          <div class="link-card" onclick="openSite('https://www.facebook.com')"><div style="background:#1877f2">f</div><p>Facebook</p></div>
        </div>
      </div>
    </div>
    <div id="pageGames" class="page">
      <div class="game-wrap">
        <h2 style="font-size:20px">🎮 Tic Tac Toe</h2>
        <div id="gameStatus">Turn: X</div>
        <div id="ttt"></div>
        <button class="btn-outline" onclick="resetGame()">🔄 Reset Game</button>
        <div class="coming"><div style="font-size:40px">🕹️</div><h3>More games coming soon!</h3><p class="muted">Racing, Puzzle, Ludo and more</p></div>
      </div>
    </div>
    <div id="pageProfile" class="page">
      <div class="profile-head">
        <div class="big-av" id="profileAvatar">H</div>
        <h2 id="profileName">HMF User</h2>
        <p class="muted" id="profileHandle">@hmfuser</p>
        <div class="stats"><div><b>12</b><span>Posts</span></div><div><b>1.2K</b><span>Followers</span></div><div><b>340</b><span>Following</span></div></div>
        <div class="pill-row"><button class="pill green" onclick="showToast('Edit profile')">Edit Profile</button><button class="pill" onclick="openSettings()">Settings</button></div>
      </div>
      <div class="grid6">
        <div class="gtile p1">🏔️</div><div class="gtile av1">📷</div><div class="gtile p2">🎵</div>
        <div class="gtile r2">🌳</div><div class="gtile p3">🎨</div><div class="gtile av2">🍛</div>
      </div>
    </div>
  </div>
  <div class="bottom-nav">
    <button class="nav-btn active" onclick="switchTab(this,'pageHome')">🏠<span>Home</span></button>
    <button class="nav-btn" onclick="switchTab(this,'pageReels')">🎬<span>Reels</span></button>
    <button class="nav-btn" onclick="switchTab(this,'pageSearch')">🔍<span>Search</span></button>
    <button class="nav-btn" onclick="switchTab(this,'pageGames')">🎮<span>Games</span></button>
    <button class="nav-btn" onclick="switchTab(this,'pageProfile')">👤<span>Profile</span></button>
  </div>
  <div id="settingsScreen">
    <div class="set-head"><button class="back-btn" onclick="closeSettings()">←</button><h2>Settings</h2></div>
    <div class="set-summary"><div class="big-av" style="width:56px;height:56px;font-size:24px" id="settingsAvatar">H</div><div><b id="settingsName">HMF User</b><br><span class="muted" id="settingsHandle">@hmfuser</span></div></div>
    <div class="set-group">
      <h4>How you use HMF</h4>
      <div class="set-row" onclick="showToast('Saved')">🔖 Saved<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('Archive')">🗂️ Archive<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('Your activity')">📊 Your Activity<span class="chev">›</span></div>
    </div>
    <div class="set-group">
      <h4>Who can see your content</h4>
      <div class="set-row" onclick="showToast('Account privacy')">🔒 Account Privacy<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('Close friends')">⭐ Close Friends<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('Blocked')">🚫 Blocked Accounts<span class="chev">›</span></div>
    </div>
    <div class="set-group">
      <h4>Your app and media</h4>
      <div class="set-row" onclick="showToast('Notifications')">🔔 Notifications<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('Time spent')">⏰ Time Spent<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('Language')">🌐 Language<span class="chev">›</span></div>
    </div>
    <div class="set-group">
      <h4>About</h4>
      <div class="set-row" onclick="showToast('Help center')">❓ Help Center<span class="chev">›</span></div>
      <div class="set-row" onclick="showToast('HMF Book v1.0')">ℹ️ About HMF Book<span class="chev">›</span></div>
      <div class="set-row danger" onclick="logout()">🚪 Log Out</div>
    </div>
    <div style="height:30px"></div>
  </div>
</div>
<div id="toast"></div>
</div>
<script>
function showScreen(id){document.querySelectorAll('.screen').forEach(function(s){s.classList.remove('active');});document.getElementById(id).classList.add('active');}
function switchTab(btn,id){document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.remove('active');});btn.classList.add('active');document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active');});document.getElementById(id).classList.add('active');closeSettings();}
function openSettings(){document.getElementById('settingsScreen').classList.add('active');}
function closeSettings(){document.getElementById('settingsScreen').classList.remove('active');}
var toastTimer;
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.classList.remove('show');},2500);}
function togglePass(id,btn){var inp=document.getElementById(id);if(inp.type==='password'){inp.type='text';btn.textContent='🙈';}else{inp.type='password';btn.textContent='👁️';}}
var hmfUser=null;
try{hmfUser=JSON.parse(localStorage.getItem('hmfUser')||'null');}catch(e){hmfUser=null;}
function saveUser(obj){hmfUser=obj;try{localStorage.setItem('hmfUser',JSON.stringify(obj));}catch(e){}}
function signup(){var u=document.getElementById('suUser').value.trim();var e=document.getElementById('suEmail').value.trim();var p=document.getElementById('suPass').value;if(!u||!e||!p){showToast('Please fill all fields');return;}if(p.length<6){showToast('Password must be 6+ characters');return;}saveUser({u:u,e:e,p:p});enterApp(u);showToast('Welcome '+u+'!');}
function login(){var e=document.getElementById('liEmail').value.trim();var p=document.getElementById('liPass').value;if(hmfUser&&hmfUser.e===e&&hmfUser.p===p){enterApp(hmfUser.u);showToast('Welcome back!');}else{showToast('Invalid email or password');}}
function socialLogin(name){var u=name+' User';saveUser({u:u,e:name.toLowerCase()+'.user@demo.com',p:'demo123'});enterApp(u);showToast(name+' login successful');}
function enterApp(name){var ini=name.charAt(0).toUpperCase();var handle='@'+name.toLowerCase().replace(/\s+/g,'');document.getElementById('profileName').textContent=name;document.getElementById('settingsName').textContent=name;document.getElementById('profileHandle').textContent=handle;document.getElementById('settingsHandle').textContent=handle;document.getElementById('profileAvatar').textContent=ini;document.getElementById('settingsAvatar').textContent=ini;document.getElementById('myStoryAvatar').textContent=ini;showScreen('app');}
function logout(){closeSettings();showScreen('splash');showToast('Logged out');}
function toggleLike(btn){if(btn.textContent==='🤍'){btn.textContent='❤️';}else{btn.textContent='🤍';}}
var lastTap=0;
function doubleLike(el){var now=Date.now();if(now-lastTap<350){var btn=el.parentElement.querySelector('.like-btn');if(btn){btn.textContent='❤️';}var h=document.createElement('div');h.className='big-heart';h.textContent='❤️';el.appendChild(h);setTimeout(function(){h.remove();},800);}lastTap=now;}
function doSearch(){var q=document.getElementById('searchInput').value.trim();if(!q){showToast('Type something to search');return;}window.open('https://www.google.com/search?q='+encodeURIComponent(q),'_blank');}
function setQuery(q){document.getElementById('searchInput').value=q;doSearch();}
function openSite(url){window.open(url,'_blank');}
var board=['','','','','','','','',''];var current='X';var gameOver=false;
function renderBoard(){var c=document.getElementById('ttt');c.innerHTML='';for(var i=0;i<9;i++){(function(i){var d=document.createElement('div');d.className='cell';d.textContent=board[i];d.onclick=function(){playCell(i);};c.appendChild(d);})(i);}}
function playCell(i){if(gameOver||board[i]!=='')return;board[i]=current;renderBoard();var w=checkWin();if(w){gameOver=true;document.getElementById('gameStatus').textContent=(w==='Draw')?'Draw!':(w+' wins!');return;}current=(current==='X')?'O':'X';document.getElementById('gameStatus').textContent='Turn: '+current;}
function checkWin(){var lines=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];for(var i=0;i<lines.length;i++){var a=lines[i][0],b=lines[i][1],c=lines[i][2];if(board[a]!==''&&board[a]===board[b]&&board[a]===board[c])return board[a];}return board.indexOf('')===-1?'Draw':null;}
function resetGame(){board=['','','','','','','','',''];current='X';gameOver=false;renderBoard();document.getElementById('gameStatus').textContent='Turn: X';}
renderBoard();
</script>
</body>
</html>
"""

components.html(APP_HTML, height=880, scrolling=True)
