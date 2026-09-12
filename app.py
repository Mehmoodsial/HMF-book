import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HMF Book", page_icon="🟢", layout="wide")

st.markdown("<style>#MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}</style>", unsafe_allow_html=True)

APP_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>HMF Book</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Arial,sans-serif;-webkit-tap-highlight-color:transparent}
html,body{width:100%;height:100%}
body{background:#fff;display:flex;justify-content:center}
.phone{width:100%;max-width:430px;min-height:100vh;background:#fff;position:relative;overflow-x:hidden}
.screen{display:none;min-height:100vh;flex-direction:column}
.screen.active{display:flex}
#splash{background:linear-gradient(140deg,#00e08a,#00b45a 45%,#009e4f);justify-content:center;align-items:center;text-align:center}
.hmf-logo{font-size:78px;font-weight:900;color:#fff;letter-spacing:2px;font-style:italic}
.hmf-sub{font-size:26px;color:#fff;font-weight:600;margin-top:6px}
.get-started{margin-top:70px;padding:15px 60px;border:none;border-radius:999px;background:#fff;color:#009e4f;font-size:19px;font-weight:800;cursor:pointer}
.auth-top{background:linear-gradient(140deg,#00e08a,#00b45a 45%,#009e4f);padding:55px 30px 85px;text-align:center}
.auth-top .hmf-logo{font-size:56px}
.auth-card{background:#fff;border-radius:28px 28px 0 0;margin-top:-45px;padding:28px 22px 40px;flex:1}
.auth-card h1{font-size:28px;color:#222;margin-bottom:20px}
.input-box{display:flex;align-items:center;gap:10px;border:1.5px solid #dfe3e8;border-radius:14px;padding:13px 14px;margin-bottom:13px}
.input-box input{border:none;outline:none;flex:1;font-size:15px;min-width:0;background:transparent}
.eye{cursor:pointer;background:none;border:none;font-size:16px}
.btn{width:100%;padding:14px;border:none;border-radius:999px;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:17px;font-weight:800;cursor:pointer;margin-top:6px}
.fp-link{text-align:right;margin:-4px 0 8px}
.fp-link a{color:#009e4f;font-weight:700;font-size:13px;cursor:pointer}
.divider{display:flex;align-items:center;gap:12px;color:#8a9299;font-size:14px;margin:20px 0 14px}
.divider:before,.divider:after{content:"";flex:1;height:1px;background:#e3e7eb}
.social-row{display:flex;justify-content:center;gap:26px}
.social{width:46px;height:46px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;cursor:pointer;border:none;color:#fff}
.g-g{background:#fff;border:2px solid #eee;color:#ea4335}
.g-s{background:#fffc00}
.g-f{background:#1877f2}
.switch-auth{text-align:center;margin-top:20px;font-size:14px;color:#5b6167}
.switch-auth a{color:#009e4f;font-weight:700;cursor:pointer}
#app{height:100vh}
.app-header{background:#fff;color:#262626;padding:12px 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #dbdbdb}
.brand{font-size:24px;font-weight:800;font-style:italic;color:#009e4f}
.header-ico{font-size:22px;cursor:pointer}
.app-header .right-icons{display:flex;gap:18px;align-items:center}
.content{flex:1;overflow-y:auto;background:#f7f8fa;-webkit-overflow-scrolling:touch}
.page{display:none}
.page.active{display:block}
.bottom-nav{display:flex;justify-content:space-around;align-items:center;background:#fff;border-top:1px solid #dbdbdb;padding:10px 0 14px}
.nav-btn{background:none;border:none;font-size:25px;line-height:1;cursor:pointer;filter:grayscale(1);opacity:.55;padding:4px 8px;transition:transform .15s,opacity .15s}
.nav-btn:active{transform:scale(.9)}
.nav-btn.active{filter:none;opacity:1;transform:scale(1.15)}
.stories{display:flex;gap:14px;overflow-x:auto;padding:14px;background:#fff;border-bottom:1px solid #eceff2}
.story{text-align:center;font-size:11px;color:#333;min-width:60px;cursor:pointer}
.story-av{width:56px;height:56px;border-radius:50%;border:2.5px solid #00d67e;padding:2.5px;display:flex;align-items:center;justify-content:center;background:#fff;margin:0 auto;overflow:hidden}
.story-av div{width:100%;height:100%;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:20px}
.story-av img{width:100%;height:100%;object-fit:cover;border-radius:50%}
.av1{background:linear-gradient(135deg,#f9ce34,#ee2a7b)}
.av2{background:linear-gradient(135deg,#667eea,#764ba2)}
.av3{background:linear-gradient(135deg,#11998e,#38ef7d)}
.av4{background:linear-gradient(135deg,#fc4a1a,#f7b733)}
.my-story .story-av{border-style:dashed;color:#009e4f;font-size:26px;font-weight:800}
.post{background:#fff;margin:12px;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.post-head{display:flex;align-items:center;gap:10px;padding:10px 12px}
.mini-av{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;flex:none;overflow:hidden}
.mini-av img{width:100%;height:100%;object-fit:cover}
.muted{color:#8a9299;font-size:12px}
.dots{margin-left:auto;font-size:20px;color:#5b6167;cursor:pointer;padding:0 4px}
.post-img{height:230px;display:flex;align-items:center;justify-content:center;font-size:74px;position:relative;cursor:pointer;user-select:none}
.p1{background:linear-gradient(135deg,#89f7fe,#66a6ff)}
.p2{background:linear-gradient(135deg,#fddb92,#d1fdff)}
.p3{background:linear-gradient(135deg,#a18cd1,#fbc2eb)}
.post-media{position:relative;background:#000}
.post-photo{width:100%;max-height:400px;object-fit:cover;display:block;cursor:pointer}
.big-heart{position:absolute;font-size:90px;animation:pop .8s ease;pointer-events:none}
@keyframes pop{0%{transform:scale(0);opacity:0}40%{transform:scale(1.2);opacity:1}100%{transform:scale(1);opacity:0}}
.post-actions{display:flex;gap:16px;padding:10px 12px;font-size:20px}
.icon-btn{background:none;border:none;font-size:20px;cursor:pointer}
.save-btn{margin-left:auto}
.caption{padding:0 12px 12px;font-size:14px;word-wrap:break-word}
.reel{height:55vh;min-height:340px;border-radius:18px;margin:12px;position:relative;display:flex;align-items:flex-end;color:#fff;overflow:hidden}
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
.search-bar input{border:none;outline:none;flex:1;font-size:15px;min-width:0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.chip{background:#fff;border:1px solid #dfe3e8;border-radius:999px;padding:8px 14px;font-size:13px;cursor:pointer}
.link-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px}
.link-card{background:#fff;border-radius:16px;padding:16px 6px;text-align:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.link-card div{width:44px;height:44px;border-radius:50%;margin:0 auto 8px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:900}
.link-card p{font-size:12px;color:#333}
.game-menu{padding:20px;text-align:center}
.games-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:14px}
.game-card{background:#fff;border-radius:16px;padding:24px 8px;text-align:center;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.05);font-size:40px}
.game-card p{font-size:13px;color:#333;margin-top:6px;font-weight:700}
.game-panel{display:none;background:#fff;margin:12px;border-radius:16px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.05)}
.game-panel.active{display:block}
.game-top{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.game-top h3{font-size:17px}
.game-back{background:none;border:2px solid #009e4f;color:#009e4f;border-radius:999px;padding:6px 14px;font-weight:700;cursor:pointer;font-size:13px}
.game-hint{font-size:12px;color:#8a9299;margin:6px 0;text-align:center}
canvas{max-width:100%;display:block;margin:0 auto;touch-action:none;border-radius:12px}
.center-wrap{display:flex;justify-content:center}
#ttt{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:290px;margin:10px auto}
.cell{aspect-ratio:1;background:#f7f8fa;border:2px solid #e3e7eb;border-radius:12px;font-size:34px;font-weight:800;color:#009e4f;display:flex;align-items:center;justify-content:center;cursor:pointer}
.btn-outline{margin-top:12px;padding:10px 26px;border:2px solid #009e4f;border-radius:999px;background:#fff;color:#009e4f;font-weight:700;cursor:pointer;font-size:14px;margin-right:6px}
#gameStatus,.gstat{font-size:16px;font-weight:700;margin:8px 0;color:#009e4f;text-align:center}
#raceScore{font-weight:700;color:#009e4f;margin-bottom:6px;text-align:center}
#raceOver{display:none;color:#ed4956;font-weight:800;margin-top:8px;text-align:center}
.race-ctrl{display:flex;justify-content:space-between;margin-top:10px;max-width:300px;margin-left:auto;margin-right:auto}
.race-ctrl button{width:80px;height:56px;font-size:24px;border:none;border-radius:14px;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-weight:800;cursor:pointer}
.ludo-row{display:flex;align-items:center;margin:10px 0;font-size:14px}
.lbar{flex:1;height:12px;background:#e9ecef;border-radius:99px;overflow:hidden;margin:0 8px}
.lp{height:100%;width:0;background:linear-gradient(135deg,#00d67e,#009e4f);transition:width .3s}
.lc{height:100%;width:0;background:linear-gradient(160deg,#ff512f,#dd2476);transition:width .3s}
.dice{font-size:46px;text-align:center;margin:10px 0;min-height:56px}
#ludoMsg{text-align:center;font-weight:700;margin-bottom:10px}
.ludo-btns{text-align:center}
#memGrid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:320px;margin:10px auto}
.mem-card{aspect-ratio:1;background:linear-gradient(135deg,#00d67e,#009e4f);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:26px;cursor:pointer;color:transparent;transition:background .2s}
.mem-card.open{background:#fff;border:2px solid #00d67e;color:#222}
.mem-card.done{background:#eafaf2;border:2px solid #9be3bd;color:#222}
.rps-row{display:flex;justify-content:space-around;align-items:center;margin:16px 0;font-size:46px}
.rps-vs{font-size:18px;font-weight:800;color:#8a9299}
.rps-btns{display:flex;gap:12px;justify-content:center}
.rps-btns button{font-size:28px;width:62px;height:62px;border-radius:50%;border:2px solid #dfe3e8;background:#fff;cursor:pointer}
.rps-btns button:active{background:#eafaf2}
#rpsResult{text-align:center;font-weight:800;margin-top:12px;min-height:22px}
.profile-head{background:#fff;padding:24px 16px;text-align:center;border-bottom:1px solid #eceff2}
.big-av{width:86px;height:86px;border-radius:50%;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:36px;font-weight:800;display:flex;align-items:center;justify-content:center;margin:0 auto 10px;overflow:hidden;cursor:pointer;border:2.5px solid #00b45a;position:relative}
.big-av img{width:100%;height:100%;object-fit:cover}
.dp-cam{position:absolute;bottom:0;right:0;background:#009e4f;color:#fff;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;border:2px solid #fff}
.stats{display:flex;justify-content:center;gap:34px;margin:16px 0}
.stats b{display:block;font-size:18px}
.stats span{font-size:12px;color:#8a9299}
.pill-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.pill{padding:9px 18px;border-radius:999px;border:1.5px solid #dfe3e8;background:#fff;font-weight:700;cursor:pointer;font-size:13px}
.pill.green{background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;border:none}
.grid6{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px}
.gtile{aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-size:38px;color:#fff}
#settingsScreen{position:absolute;top:0;left:0;right:0;bottom:0;background:#f3f4f6;overflow-y:auto;display:none;z-index:50}
#settingsScreen.active{display:block}
.set-head{background:linear-gradient(140deg,#00e08a,#009e4f);color:#fff;padding:16px 18px 20px;display:flex;align-items:center;gap:14px}
.back-btn{background:none;border:none;color:#fff;font-size:22px;cursor:pointer}
.set-summary{background:#fff;margin:14px;border-radius:16px;padding:16px;display:flex;gap:14px;align-items:center}
.set-av{width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:24px;font-weight:800;display:flex;align-items:center;justify-content:center;overflow:hidden;flex:none}
.set-av img{width:100%;height:100%;object-fit:cover}
.set-group{background:#fff;margin:14px;border-radius:16px;overflow:hidden}
.set-group h4{padding:12px 16px 4px;color:#009e4f;font-size:13px;text-transform:uppercase}
.set-row{display:flex;align-items:center;gap:12px;padding:14px 16px;border-top:1px solid #f0f2f4;cursor:pointer;font-size:15px}
.set-row .chev{margin-left:auto;color:#b3b9bf}
.set-row.danger{color:#ed4956}
#toast{position:fixed;bottom:95px;left:50%;transform:translateX(-50%);background:#222;color:#fff;padding:11px 20px;border-radius:999px;font-size:14px;opacity:0;pointer-events:none;transition:.3s;z-index:110;max-width:88%;text-align:center}
#toast.show{opacity:1}
#msgScreen{position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:none;z-index:60;flex-direction:column}
#msgScreen.active{display:flex}
.msg-head{background:linear-gradient(140deg,#00e08a,#009e4f);color:#fff;padding:14px 16px;display:flex;align-items:center;gap:12px}
.msg-head h2{font-size:18px}
.msg-tabs{display:flex;background:#fff;border-bottom:1px solid #eceff2}
.msg-tab{flex:1;padding:12px;font-size:24px;background:none;border:none;cursor:pointer;opacity:.4;border-bottom:3px solid transparent}
.msg-tab.active{opacity:1;border-bottom-color:#00b45a}
.msg-list{flex:1;overflow-y:auto;display:none}
.msg-list.active{display:block}
.chat-row{display:flex;align-items:center;gap:12px;padding:12px 16px;cursor:pointer;border-bottom:1px solid #f3f4f6}
.chat-av{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:20px;flex:none;overflow:hidden}
.chat-av img{width:100%;height:100%;object-fit:cover}
.chat-info{flex:1;min-width:0}
.chat-info b{font-size:15px}
.chat-info p{font-size:13px;color:#8a9299;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chat-time{font-size:11px;color:#b3b9bf;flex:none}
.snap-av{background:#fffc00;color:#fff;border-radius:16px}
.new-snap p{color:#ed4956;font-weight:700}
#chatView{position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:none;z-index:70;flex-direction:column}
#chatView.active{display:flex}
.chat-body{flex:1;overflow-y:auto;padding:16px;background:#f7f8fa;display:flex;flex-direction:column;gap:8px}
.bubble-row{display:flex;align-items:center;gap:6px}
.bubble-row.me{align-self:flex-end;justify-content:flex-end}
.bubble-row.them{align-self:flex-start}
.bubble{max-width:75%;padding:10px 14px;border-radius:18px;font-size:14px;line-height:1.4;word-wrap:break-word}
.bubble.me{background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;border-bottom-right-radius:4px}
.bubble.them{background:#e9ecef;color:#333;border-bottom-left-radius:4px}
.unsend-btn{background:none;border:none;color:#c7ccd1;font-size:12px;cursor:pointer;padding:2px}
.sys-note{align-self:center;font-size:11px;color:#8a9299;font-style:italic;background:#e4e7ea;padding:4px 12px;border-radius:999px}
.chat-input{display:flex;gap:8px;padding:10px;border-top:1px solid #eceff2;background:#fff}
.chat-input input{flex:1;border:1.5px solid #dfe3e8;border-radius:999px;padding:11px 16px;font-size:14px;outline:none;min-width:0}
.chat-input button{width:44px;height:44px;border:none;border-radius:50%;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:18px;cursor:pointer;flex:none}
#createScreen{position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:none;z-index:65;flex-direction:column}
#createScreen.active{display:flex}
.create-body{flex:1;overflow-y:auto;padding:20px}
#pickArea{border:2px dashed #b8c4bc;border-radius:18px;padding:44px 20px;text-align:center;cursor:pointer;color:#5b6167;background:#fafbfa}
#previewWrap{display:none}
#previewWrap img{width:100%;max-height:300px;object-fit:cover;border-radius:14px;display:block}
#previewWrap video{width:100%;max-height:300px;border-radius:14px;display:block;background:#000}
#editScreen{position:absolute;top:0;left:0;right:0;bottom:0;background:#fff;display:none;z-index:75;flex-direction:column}
#editScreen.active{display:flex}
.edit-body{flex:1;overflow-y:auto;padding:20px;text-align:center}
.dp-wrap{position:relative;width:110px;margin:14px auto}
.dp-main{width:110px;height:110px;border-radius:50%;background:linear-gradient(135deg,#00d67e,#009e4f);color:#fff;font-size:44px;font-weight:800;display:flex;align-items:center;justify-content:center;overflow:hidden;cursor:pointer;border:3px solid #00b45a}
.dp-main img{width:100%;height:100%;object-fit:cover}
.dp-cam2{position:absolute;bottom:0;right:0;background:#009e4f;color:#fff;width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;border:2px solid #fff;cursor:pointer}
.edit-label{text-align:left;font-size:12px;color:#8a9299;margin:16px 0 6px;text-transform:uppercase;font-weight:700}
.edit-input{width:100%;border:1.5px solid #dfe3e8;border-radius:12px;padding:12px 14px;font-size:15px;outline:none}
.edit-input:focus{border-color:#00b45a}
textarea.edit-input{resize:vertical;min-height:70px;font-family:inherit}
.done-btn{background:none;border:none;color:#fff;font-size:15px;font-weight:700;cursor:pointer;margin-left:auto}
#sheetBackdrop{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.45);display:none;z-index:80}
#sheetBackdrop.active{display:block}
#sheet{position:fixed;left:50%;bottom:-100%;transform:translateX(-50%);width:100%;max-width:430px;background:#fff;border-radius:20px 20px 0 0;z-index:81;transition:bottom .25s;padding:8px 0 18px}
#sheet.active{bottom:0}
.sheet-handle{width:40px;height:4px;background:#dfe3e8;border-radius:99px;margin:6px auto 10px}
.sheet-item{padding:15px 24px;font-size:15px;cursor:pointer;border-top:1px solid #f3f4f6}
.sheet-item.danger{color:#ed4956;font-weight:700}
.sheet-item.cancel{color:#8a9299;text-align:center;font-weight:700}
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
    <div class="input-box">🔒<input id="suPass" type="password" placeholder="Password (6+ chars)"><button class="eye" onclick="togglePass('suPass',this)">👁️</button></div>
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
    <p class="fp-link"><a onclick="openForgot()">Forgot password?</a></p>
    <button class="btn" onclick="login()">Log In</button>
    <div id="forgotBox" style="display:none;margin-top:14px;border-top:1px solid #eceff2;padding-top:14px">
      <p style="font-weight:700;font-size:14px;margin-bottom:10px">🔑 Reset Password</p>
      <div class="input-box">✉️<input id="fpEmail" type="email" placeholder="Your registered email"></div>
      <button class="btn" onclick="findAccount()">Find Account</button>
      <div id="fpReset" style="display:none">
        <div class="input-box" style="margin-top:12px">🔒<input id="fpNew" type="password" placeholder="New password (6+ chars)"></div>
        <button class="btn" onclick="resetPassword()">Reset Password</button>
      </div>
    </div>
    <p class="switch-auth">New here? <a onclick="showScreen('auth')">Create Account</a></p>
  </div>
</div>
<div id="app" class="screen">
  <div class="app-header">
    <div class="brand">HMF book</div>
    <div class="right-icons">
      <span class="header-ico" onclick="openCreate()" title="Create Post">➕</span>
      <span class="header-ico" onclick="openMessages()">📩</span>
      <span class="header-ico" onclick="openSettings()">⚙️</span>
    </div>
  </div>
  <div class="content">
    <div id="pageHome" class="page active">
      <div class="stories">
        <div class="story my-story" onclick="openCreate()"><div class="story-av"><div id="myStoryAvatar">+</div></div>Your story</div>
        <div class="story"><div class="story-av"><div class="av1">A</div></div>Ahmed</div>
        <div class="story"><div class="story-av"><div class="av2">S</div></div>Sara</div>
        <div class="story"><div class="story-av"><div class="av3">B</div></div>Bilal</div>
        <div class="story"><div class="story-av"><div class="av4">Z</div></div>Zara</div>
      </div>
      <div class="post" id="postDemo1">
        <div class="post-head"><div class="mini-av av1">A</div><div><b>Ahmed</b><br><span class="muted">Hunza Valley</span></div><span class="dots" onclick="openSheet(this.closest('.post'))">⋯</span></div>
        <div class="post-img p1" onclick="doubleLike(this)">🏔️</div>
        <div class="post-actions"><button class="icon-btn like-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="openSheet(this.closest('.post'))">🔗</button><button class="icon-btn save-btn" onclick="downloadPost(this.closest('.post'))">⬇️</button></div>
        <div class="caption"><b>Ahmed</b> Beautiful Pakistan 🇵🇰</div>
      </div>
      <div class="post" id="postDemo2">
        <div class="post-head"><div class="mini-av av2">S</div><div><b>Sara</b><br><span class="muted">Original audio</span></div><span class="dots" onclick="openSheet(this.closest('.post'))">⋯</span></div>
        <div class="post-img p2" onclick="doubleLike(this)">🎵</div>
        <div class="post-actions"><button class="icon-btn like-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="openSheet(this.closest('.post'))">🔗</button><button class="icon-btn save-btn" onclick="downloadPost(this.closest('.post'))">⬇️</button></div>
        <div class="caption"><b>Sara</b> New reel trend! 🔥</div>
      </div>
      <div class="post" id="postDemo3">
        <div class="post-head"><div class="mini-av av3">B</div><div><b>Bilal</b><br><span class="muted">Gaming</span></div><span class="dots" onclick="openSheet(this.closest('.post'))">⋯</span></div>
        <div class="post-img p3" onclick="doubleLike(this)">🎮</div>
        <div class="post-actions"><button class="icon-btn like-btn" onclick="toggleLike(this)">🤍</button><button class="icon-btn" onclick="showToast('Comments')">💬</button><button class="icon-btn" onclick="openSheet(this.closest('.post'))">🔗</button><button class="icon-btn save-btn" onclick="downloadPost(this.closest('.post'))">⬇️</button></div>
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
      <div class="game-menu" id="gameMenu">
        <h2 style="font-size:22px">🎮 HMF Games</h2>
        <div class="games-grid">
          <div class="game-card" onclick="showGame('gRace')">🏎️<p>Car Racing</p></div>
          <div class="game-card" onclick="showGame('gLudo')">🎲<p>Ludo Race</p></div>
          <div class="game-card" onclick="showGame('gSnk')">🎱<p>Snooker</p></div>
          <div class="game-card" onclick="showGame('gTTT')">⭕<p>Tic Tac Toe</p></div>
          <div class="game-card" onclick="showGame('gMem')">🧠<p>Memory</p></div>
          <div class="game-card" onclick="showGame('gRPS')">✊<p>Rock Paper</p></div>
        </div>
      </div>
      <div class="game-panel" id="gRace">
        <div class="game-top"><button class="game-back" onclick="backToGames()">← Games</button><h3>🏎️ Car Racing</h3></div>
        <div id="raceScore">Score: 0</div>
        <div class="center-wrap"><canvas id="raceCanvas" width="300" height="400" style="background:#2c3e50"></canvas></div>
        <div id="raceOver">💥 Crash! Tap Start again</div>
        <div class="race-ctrl"><button onclick="raceMove(-1)">◀</button><button onclick="startRace()">▶ Start</button><button onclick="raceMove(1)">▶</button></div>
        <p class="game-hint">Keyboard: Left/Right arrows bhi chalte hain</p>
      </div>
      <div class="game-panel" id="gLudo">
        <div class="game-top"><button class="game-back" onclick="backToGames()">← Games</button><h3>🎲 Ludo Race</h3></div>
        <div class="ludo-row"><span>🧑 You</span><div class="lbar"><div id="ludoPBar" class="lp"></div></div><span id="ludoPStep">0/30</span></div>
        <div class="ludo-row"><span>🤖 CPU</span><div class="lbar"><div id="ludoCBar" class="lc"></div></div><span id="ludoCStep">0/30</span></div>
        <div class="dice" id="ludoDice">🎲</div>
        <div id="ludoMsg">Your turn — Roll!</div>
        <div class="ludo-btns"><button class="btn-outline" onclick="ludoRoll()">🎲 Roll</button><button class="btn-outline" onclick="ludoReset()">Reset</button></div>
        <p class="game-hint">Pehle 30 tak pohnchne wala jeeta!</p>
      </div>
      <div class="game-panel" id="gSnk">
        <div class="game-top"><button class="game-back" onclick="backToGames()">← Games</button><h3>🎱 Snooker</h3></div>
        <div class="gstat" id="snkScore">Potted: 0 / 3</div>
        <div class="center-wrap"><canvas id="snkCanvas" width="300" height="480"></canvas></div>
        <p class="game-hint">Drag karke peeche kheenchein (pull back) aur chhod dein — shot lagega!</p>
        <div class="ludo-btns"><button class="btn-outline" onclick="startSnooker()">🔄 Re-rack</button></div>
      </div>
      <div class="game-panel" id="gTTT">
        <div class="game-top"><button class="game-back" onclick="backToGames()">← Games</button><h3>⭕ Tic Tac Toe</h3></div>
        <div id="gameStatus">Turn: X</div>
        <div id="ttt"></div>
        <div class="ludo-btns"><button class="btn-outline" onclick="resetGame()">🔄 Reset</button></div>
      </div>
      <div class="game-panel" id="gMem">
        <div class="game-top"><button class="game-back" onclick="backToGames()">← Games</button><h3>🧠 Memory Match</h3></div>
        <div class="gstat" id="memMoves">Moves: 0</div>
        <div id="memGrid"></div>
        <div class="ludo-btns"><button class="btn-outline" onclick="startMemory()">🔄 New Game</button></div>
      </div>
      <div class="game-panel" id="gRPS">
        <div class="game-top"><button class="game-back" onclick="backToGames()">← Games</button><h3>✊ Rock Paper Scissors</h3></div>
        <div class="rps-row"><span id="rpsYou">❔</span><span class="rps-vs">VS</span><span id="rpsComp">🤖</span></div>
        <div id="rpsResult">Choose one!</div>
        <div class="rps-btns">
          <button onclick="rpsPlay('rock')">✊</button>
          <button onclick="rpsPlay('paper')">✋</button>
          <button onclick="rpsPlay('scissors')">✌️</button>
        </div>
      </div>
    </div>
    <div id="pageProfile" class="page">
      <div class="profile-head">
        <div class="big-av" id="profileAvatar" onclick="openEdit()" title="Change DP">H<div class="dp-cam">📷</div></div>
        <h2 id="profileName">HMF User</h2>
        <p class="muted" id="profileHandle">@hmfuser</p>
        <p style="font-size:14px;margin-top:6px" id="profileBio"></p>
        <div class="stats"><div><b id="postCount">12</b><span>Posts</span></div><div><b>1.2K</b><span>Followers</span></div><div><b>340</b><span>Following</span></div></div>
        <div class="pill-row">
          <button class="pill green" onclick="openCreate()">➕ New Post</button>
          <button class="pill" onclick="openEdit()">✏️ Edit Profile</button>
          <button class="pill" onclick="openSettings()">⚙️ Settings</button>
        </div>
      </div>
      <div class="grid6">
        <div class="gtile p1">🏔️</div><div class="gtile av1">📷</div><div class="gtile p2">🎵</div>
        <div class="gtile r2">🌳</div><div class="gtile p3">🎨</div><div class="gtile av2">🍛</div>
      </div>
    </div>
  </div>
  <div class="bottom-nav">
    <button class="nav-btn active" onclick="switchTab(this,'pageHome')">🏠</button>
    <button class="nav-btn" onclick="switchTab(this,'pageSearch')">🔍</button>
    <button class="nav-btn" onclick="switchTab(this,'pageReels')">🎬</button>
    <button class="nav-btn" onclick="switchTab(this,'pageGames')">🎮</button>
    <button class="nav-btn" onclick="switchTab(this,'pageProfile')">👤</button>
  </div>
  <div id="settingsScreen">
    <div class="set-head"><button class="back-btn" onclick="closeSettings()">←</button><h2>Settings</h2></div>
    <div class="set-summary"><div class="set-av" id="settingsAvatar">H</div><div><b id="settingsName">HMF User</b><br><span class="muted" id="settingsHandle">@hmfuser</span></div></div>
    <div class="set-group">
      <h4>Account</h4>
      <div class="set-row" onclick="openEdit()">✏️ Edit Profile / DP<span class="chev">›</span></div>
      <div class="set-row" onclick="openCreate()">➕ Create New Post<span class="chev">›</span></div>
      <div class="set-row" onclick="openMessages()">📩 Messages<span class="chev">›</span></div>
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
      <div class="set-row" onclick="showToast('HMF Book v4.0 Final')">ℹ️ About HMF Book<span class="chev">›</span></div>
      <div class="set-row danger" onclick="logout()">🚪 Log Out</div>
    </div>
    <div style="height:30px"></div>
  </div>
  <div id="createScreen">
    <div class="msg-head"><button class="back-btn" onclick="closeCreate()">←</button><h2>Create New Post</h2></div>
    <div class="create-body">
      <input type="file" id="filePick" accept="image/*,video/*" style="display:none" onchange="fileChosen(this)">
      <div id="pickArea" onclick="document.getElementById('filePick').click()">
        <div style="font-size:54px">🖼️</div>
        <p style="margin-top:8px"><b>Tap to select photo or video</b></p>
        <p class="muted" style="margin-top:4px">Max 15MB</p>
      </div>
      <div id="previewWrap"></div>
      <div class="input-box" style="margin-top:14px">✏️<input id="postCaption" type="text" placeholder="Write a caption..."></div>
      <button class="btn" onclick="publishPost()">Share Post</button>
    </div>
  </div>
  <div id="editScreen">
    <div class="msg-head"><button class="back-btn" onclick="closeEdit()">←</button><h2>Edit Profile</h2><button class="done-btn" onclick="saveProfile()">Done ✓</button></div>
    <div class="edit-body">
      <input type="file" id="dpPick" accept="image/*" style="display:none" onchange="dpChosen(this)">
      <div class="dp-wrap">
        <div class="dp-main" id="dpMain" onclick="document.getElementById('dpPick').click()">H</div>
        <div class="dp-cam2" onclick="document.getElementById('dpPick').click()">📷</div>
      </div>
      <p class="muted">Tap photo to change DP</p>
      <div class="edit-label">Name</div>
      <input class="edit-input" id="editName" type="text" placeholder="Your name">
      <div class="edit-label">Username (ID)</div>
      <input class="edit-input" id="editHandle" type="text" placeholder="username">
      <div class="edit-label">Bio</div>
      <textarea class="edit-input" id="editBio" placeholder="Write something about you..."></textarea>
    </div>
  </div>
  <div id="msgScreen">
    <div class="msg-head"><button class="back-btn" onclick="closeMessages()">←</button><h2>Messages</h2></div>
    <div class="msg-tabs">
      <button class="msg-tab active" onclick="switchMsgTab(this,'instaList')">📷</button>
      <button class="msg-tab" onclick="switchMsgTab(this,'tiktokList')">🎵</button>
      <button class="msg-tab" onclick="switchMsgTab(this,'snapList')">👻</button>
    </div>
    <div class="msg-list active" id="instaList">
      <div class="chat-row" onclick="openChatView('Ahmed','av1','A')"><div class="chat-av av1">A</div><div class="chat-info"><b>Ahmed</b><p>Sent a photo 📸</p></div><span class="chat-time">2m</span></div>
      <div class="chat-row" onclick="openChatView('Sara','av2','S')"><div class="chat-av av2">S</div><div class="chat-info"><b>Sara</b><p>Reacted ❤️ to your story</p></div><span class="chat-time">15m</span></div>
      <div class="chat-row" onclick="openChatView('Bilal','av3','B')"><div class="chat-av av3">B</div><div class="chat-info"><b>Bilal</b><p>Game khelo ge? 🎮</p></div><span class="chat-time">1h</span></div>
      <div class="chat-row" onclick="openChatView('Zara','av4','Z')"><div class="chat-av av4">Z</div><div class="chat-info"><b>Zara</b><p>Shared a reel 🎬</p></div><span class="chat-time">3h</span></div>
      <div class="chat-row" onclick="openChatView('Usman','av1','U')"><div class="chat-av av1">U</div><div class="chat-info"><b>Usman</b><p>Salam! Kya haal hai?</p></div><span class="chat-time">1d</span></div>
    </div>
    <div class="msg-list" id="tiktokList">
      <div class="chat-row" onclick="openChatView('trendstar','r1','T')"><div class="chat-av r1">T</div><div class="chat-info"><b>trendstar</b><p>Sent you a video 🎵</p></div><span class="chat-time">5m</span></div>
      <div class="chat-row" onclick="openChatView('funny.pets','r2','F')"><div class="chat-av r2">F</div><div class="chat-info"><b>funny.pets</b><p>Haha dekho ye 😹</p></div><span class="chat-time">30m</span></div>
      <div class="chat-row" onclick="openChatView('dance.queen','r1','D')"><div class="chat-av r1">D</div><div class="chat-info"><b>dance.queen</b><p>New trend try karo! 💃</p></div><span class="chat-time">2h</span></div>
      <div class="chat-row" onclick="openChatView('sports.hub','r3','S')"><div class="chat-av r3">S</div><div class="chat-info"><b>sports.hub</b><p>Match dekha? ⚽</p></div><span class="chat-time">5h</span></div>
    </div>
    <div class="msg-list" id="snapList">
      <div class="chat-row new-snap" onclick="openChatView('Ahmed','snap-av','👻')"><div class="chat-av snap-av">👻</div><div class="chat-info"><b>Ahmed</b><p>New Snap 🔴</p></div><span class="chat-time">🔥 56</span></div>
      <div class="chat-row" onclick="openChatView('Sara','snap-av','👻')"><div class="chat-av snap-av">👻</div><div class="chat-info"><b>Sara</b><p>Delivered</p></div><span class="chat-time">🔥 120</span></div>
      <div class="chat-row" onclick="openChatView('Bilal','snap-av','👻')"><div class="chat-av snap-av">👻</div><div class="chat-info"><b>Bilal</b><p>Opened</p></div><span class="chat-time">🔥 34</span></div>
      <div class="chat-row new-snap" onclick="openChatView('Bestie','snap-av','👻')"><div class="chat-av snap-av">👻</div><div class="chat-info"><b>Bestie</b><p>New Snap 🔴</p></div><span class="chat-time">🔥 365</span></div>
    </div>
    <div id="chatView">
      <div class="msg-head"><button class="back-btn" onclick="closeChatView()">←</button><div class="chat-av" id="chatUserAv" style="width:36px;height:36px;font-size:15px">A</div><h2 id="chatUserName">Chat</h2></div>
      <div class="chat-body" id="chatBody"></div>
      <div class="chat-input"><input id="msgInput" type="text" placeholder="Message..." onkeydown="if(event.key==='Enter')sendMsg()"><button onclick="sendMsg()">➤</button></div>
    </div>
  </div>
</div>
<div id="sheetBackdrop" onclick="closeSheet()"></div>
<div id="sheet">
  <div class="sheet-handle"></div>
  <div class="sheet-item" onclick="sheetCopy()">🔗 Copy Link</div>
  <div class="sheet-item" onclick="sheetSave()">⬇️ Save / Download</div>
  <div class="sheet-item danger" onclick="sheetDelete()">🗑️ Delete Post</div>
  <div class="sheet-item cancel" onclick="closeSheet()">Cancel</div>
</div>
<div id="toast"></div>
</div>
<script>
function showScreen(id){document.querySelectorAll('.screen').forEach(function(s){s.classList.remove('active');});document.getElementById(id).classList.add('active');}
function switchTab(btn,id){document.querySelectorAll('.nav-btn').forEach(function(b){b.classList.remove('active');});btn.classList.add('active');document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active');});document.getElementById(id).classList.add('active');closeSettings();closeMessages();closeCreate();closeEdit();backToGames();}
function openSettings(){closeMessages();closeCreate();closeEdit();document.getElementById('settingsScreen').classList.add('active');}
function closeSettings(){document.getElementById('settingsScreen').classList.remove('active');}
function openMessages(){closeSettings();closeCreate();closeEdit();document.getElementById('msgScreen').classList.add('active');}
function closeMessages(){document.getElementById('msgScreen').classList.remove('active');closeChatView();}
function switchMsgTab(btn,id){document.querySelectorAll('.msg-tab').forEach(function(b){b.classList.remove('active');});btn.classList.add('active');document.querySelectorAll('.msg-list').forEach(function(l){l.classList.remove('active');});document.getElementById(id).classList.add('active');}
var toastTimer;
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(function(){t.classList.remove('show');},2500);}
function togglePass(id,btn){var inp=document.getElementById(id);if(inp.type==='password'){inp.type='text';btn.textContent='🙈';}else{inp.type='password';btn.textContent='👁️';}}
function loadUsers(){try{return JSON.parse(localStorage.getItem('hmfUsers')||'{}');}catch(e){return {};}}
function saveUsers(u){try{localStorage.setItem('hmfUsers',JSON.stringify(u));}catch(e){}}
function loadProfiles(){try{return JSON.parse(localStorage.getItem('hmfProfiles')||'{}');}catch(e){return {};}}
function saveProfiles(p){try{localStorage.setItem('hmfProfiles',JSON.stringify(p));}catch(e){}}
var currentUser=null;
var profile={name:'HMF User',handle:'hmfuser',bio:'',dp:null};
function persistProfile(){if(!currentUser)return;var all=loadProfiles();all[currentUser]=profile;saveProfiles(all);}
function setAvatar(el){if(!el)return;if(profile.dp){el.innerHTML='<img src="'+profile.dp+'">';}else{el.textContent=profile.name.charAt(0).toUpperCase();}}
function applyProfileEverywhere(){document.getElementById('profileName').textContent=profile.name;document.getElementById('settingsName').textContent=profile.name;document.getElementById('profileHandle').textContent='@'+profile.handle;document.getElementById('settingsHandle').textContent='@'+profile.handle;document.getElementById('profileBio').textContent=profile.bio;setAvatar(document.getElementById('profileAvatar'));setAvatar(document.getElementById('settingsAvatar'));setAvatar(document.getElementById('myStoryAvatar'));}
function openEdit(){closeSettings();closeMessages();closeCreate();document.getElementById('editName').value=profile.name;document.getElementById('editHandle').value=profile.handle;document.getElementById('editBio').value=profile.bio;setAvatar(document.getElementById('dpMain'));document.getElementById('editScreen').classList.add('active');}
function closeEdit(){document.getElementById('editScreen').classList.remove('active');}
function dpChosen(inp){var f=inp.files&&inp.files[0];if(!f)return;if(f.size>5*1024*1024){showToast('DP 5MB se choti honi chahiye');inp.value='';return;}var r=new FileReader();r.onload=function(e){profile.dp=e.target.result;setAvatar(document.getElementById('dpMain'));persistProfile();applyProfileEverywhere();showToast('DP updated ✅');};r.readAsDataURL(f);}
function saveProfile(){var n=document.getElementById('editName').value.trim();var h=document.getElementById('editHandle').value.trim();var b=document.getElementById('editBio').value.trim();if(!n){showToast('Name required');return;}profile.name=n;profile.handle=h?h.replace(/\s+/g,'').toLowerCase():'hmfuser';profile.bio=b;persistProfile();applyProfileEverywhere();closeEdit();showToast('Profile saved ✅');}
function signup(){var u=document.getElementById('suUser').value.trim();var e=document.getElementById('suEmail').value.trim().toLowerCase();var p=document.getElementById('suPass').value;if(!u||!e||!p){showToast('Please fill all fields');return;}if(p.length<6){showToast('Password must be 6+ characters');return;}var users=loadUsers();if(users[e]){showToast('Email already registered — Log in karein');return;}users[e]={u:u,e:e,p:p};saveUsers(users);var profiles=loadProfiles();if(!profiles[e]){profiles[e]={name:u,handle:u.toLowerCase().replace(/\s+/g,''),bio:'New on HMF Book 🌟',dp:null};saveProfiles(profiles);}currentUser=e;try{localStorage.setItem('hmfSession',e);}catch(err){}profile=profiles[e];applyProfileEverywhere();showScreen('app');showToast('Welcome '+u+'!');}
function login(){var e=document.getElementById('liEmail').value.trim().toLowerCase();var p=document.getElementById('liPass').value;var users=loadUsers();if(users[e]&&users[e].p===p){currentUser=e;try{localStorage.setItem('hmfSession',e);}catch(err){}var profiles=loadProfiles();profile=profiles[e]||{name:users[e].u,handle:'hmfuser',bio:'',dp:null};applyProfileEverywhere();showScreen('app');showToast('Welcome back '+profile.name+'!');}else{showToast('Invalid email or password');}}
function openForgot(){document.getElementById('forgotBox').style.display='block';document.getElementById('fpReset').style.display='none';fpUser=null;}
var fpUser=null;
function findAccount(){var e=document.getElementById('fpEmail').value.trim().toLowerCase();var users=loadUsers();if(users[e]){fpUser=e;document.getElementById('fpReset').style.display='block';showToast('Account mila! Ab naya password set karein');}else{showToast('Is email se koi account nahi');}}
function resetPassword(){if(!fpUser){showToast('Pehle email verify karein');return;}var p=document.getElementById('fpNew').value;if(p.length<6){showToast('Password 6+ characters');return;}var users=loadUsers();users[fpUser].p=p;saveUsers(users);showToast('Password reset ✅ Ab login karein');document.getElementById('forgotBox').style.display='none';}
function socialLogin(name){var u=name+' User';var e=name.toLowerCase()+'.user@demo.com';var users=loadUsers();if(!users[e]){users[e]={u:u,e:e,p:'demo123'};saveUsers(users);}var profiles=loadProfiles();if(!profiles[e]){profiles[e]={name:u,handle:name.toLowerCase()+'user',bio:'Using '+name+' 👋',dp:null};saveProfiles(profiles);}currentUser=e;try{localStorage.setItem('hmfSession',e);}catch(err){}profile=profiles[e];applyProfileEverywhere();showScreen('app');showToast(name+' login successful');}
function logout(){try{localStorage.removeItem('hmfSession');}catch(e){}currentUser=null;closeSettings();closeMessages();closeCreate();closeEdit();showScreen('splash');showToast('Logged out');}
function tryAutoLogin(){var s=null;try{s=localStorage.getItem('hmfSession');}catch(e){}if(!s)return;var users=loadUsers();if(users[s]){currentUser=s;var profiles=loadProfiles();profile=profiles[s]||{name:users[s].u,handle:'hmfuser',bio:'',dp:null};applyProfileEverywhere();showScreen('app');}}
function toggleLike(btn){if(btn.textContent==='🤍'){btn.textContent='❤️';showToast('Liked ❤️');}else{btn.textContent='🤍';}}
var lastTap=0;
function doubleLike(el){var now=Date.now();if(now-lastTap<350){var post=el.closest('.post');if(post){var btn=post.querySelector('.like-btn');if(btn){btn.textContent='❤️';}}var h=document.createElement('div');h.className='big-heart';h.textContent='❤️';el.appendChild(h);setTimeout(function(){h.remove();},800);}lastTap=now;}
function doSearch(){var q=document.getElementById('searchInput').value.trim();if(!q){showToast('Type something to search');return;}window.open('https://www.google.com/search?q='+encodeURIComponent(q),'_blank');}
function setQuery(q){document.getElementById('searchInput').value=q;doSearch();}
function openSite(url){window.open(url,'_blank');}
var replies=['Hi! 😊','Kya haal hai?','Sounds good! 👍','Haha 😄','Okay done!','Acha? Phir kya hua?','Interesting... batao aur','Main bhi soch raha tha yehi 🤔','Cool! 🎉'];
function openChatView(name,avClass,letter){document.getElementById('chatUserName').textContent=name;var av=document.getElementById('chatUserAv');av.className='chat-av '+avClass;av.style.width='36px';av.style.height='36px';av.style.fontSize='15px';av.textContent=letter;document.getElementById('chatView').classList.add('active');document.getElementById('chatBody').innerHTML='';setTimeout(function(){addBubble('them','Hi! 👋');},400);}
function closeChatView(){document.getElementById('chatView').classList.remove('active');}
function addBubble(who,text){var wrap=document.createElement('div');wrap.className='bubble-row '+who;var b=document.createElement('div');b.className='bubble '+who;b.textContent=text;if(who==='me'){var x=document.createElement('button');x.className='unsend-btn';x.textContent='✕';x.title='Unsend';x.onclick=function(){unsendMsg(wrap);};wrap.appendChild(b);wrap.appendChild(x);}else{wrap.appendChild(b);}var body=document.getElementById('chatBody');body.appendChild(wrap);body.scrollTop=body.scrollHeight;}
function unsendMsg(wrap){var n=document.createElement('div');n.className='sys-note';n.textContent='You unsent a message';wrap.parentNode.replaceChild(n,wrap);}
function sendMsg(){var inp=document.getElementById('msgInput');var t=inp.value.trim();if(!t)return;addBubble('me',t);inp.value='';setTimeout(function(){addBubble('them',replies[Math.floor(Math.random()*replies.length)]);},1000);}
var pendingMedia=null;
function openCreate(){closeSettings();closeMessages();closeEdit();document.getElementById('createScreen').classList.add('active');document.getElementById('previewWrap').style.display='none';document.getElementById('previewWrap').innerHTML='';document.getElementById('pickArea').style.display='block';document.getElementById('postCaption').value='';document.getElementById('filePick').value='';pendingMedia=null;}
function closeCreate(){document.getElementById('createScreen').classList.remove('active');}
function fileChosen(inp){var f=inp.files&&inp.files[0];if(!f)return;if(f.size>15*1024*1024){showToast('File 15MB se choti honi chahiye');inp.value='';return;}var r=new FileReader();r.onload=function(e){var isVideo=f.type.indexOf('video')===0;pendingMedia={url:e.target.result,type:isVideo?'video':'image'};var w=document.getElementById('previewWrap');w.innerHTML='';if(isVideo){var v=document.createElement('video');v.src=pendingMedia.url;v.controls=true;w.appendChild(v);}else{var im=document.createElement('img');im.src=pendingMedia.url;w.appendChild(im);}w.style.display='block';document.getElementById('pickArea').style.display='none';};r.readAsDataURL(f);}
function publishPost(){if(!pendingMedia){showToast('Pehle photo/video choose karein');return;}var cap=document.getElementById('postCaption').value.trim();if(!cap)cap='My new post ✨';var post=document.createElement('div');post.className='post';post.id='post'+Date.now();var head=document.createElement('div');head.className='post-head';var av=document.createElement('div');av.className='mini-av';setAvatar(av);var info=document.createElement('div');var b=document.createElement('b');b.textContent=profile.name;info.appendChild(b);info.appendChild(document.createElement('br'));var mu=document.createElement('span');mu.className='muted';mu.textContent='Just now';info.appendChild(mu);var dots=document.createElement('span');dots.className='dots';dots.textContent='⋯';dots.onclick=function(){openSheet(post);};head.appendChild(av);head.appendChild(info);head.appendChild(dots);var media=document.createElement('div');media.className='post-media';if(pendingMedia.type==='video'){var v=document.createElement('video');v.src=pendingMedia.url;v.controls=true;media.appendChild(v);}else{var im=document.createElement('img');im.className='post-photo';im.src=pendingMedia.url;im.onclick=function(){doubleLike(im);};media.appendChild(im);}var acts=document.createElement('div');acts.className='post-actions';var l=document.createElement('button');l.className='icon-btn like-btn';l.textContent='🤍';l.onclick=function(){toggleLike(l);};var c1=document.createElement('button');c1.className='icon-btn';c1.textContent='💬';c1.onclick=function(){showToast('Comments');};var c2=document.createElement('button');c2.className='icon-btn';c2.textContent='🔗';c2.onclick=function(){openSheet(post);};var sv=document.createElement('button');sv.className='icon-btn save-btn';sv.textContent='⬇️';sv.onclick=function(){downloadPost(post);};acts.appendChild(l);acts.appendChild(c1);acts.appendChild(c2);acts.appendChild(sv);var capEl=document.createElement('div');capEl.className='caption';var cb=document.createElement('b');cb.textContent=profile.name;capEl.appendChild(cb);capEl.appendChild(document.createTextNode(' '+cap));post.appendChild(head);post.appendChild(media);post.appendChild(acts);post.appendChild(capEl);var home=document.getElementById('pageHome');var first=home.querySelector('.post');if(first){home.insertBefore(post,first);}else{home.appendChild(post);}var pc=document.getElementById('postCount');pc.textContent=parseInt(pc.textContent)+1;closeCreate();showToast('Post shared ✅');}
var menuPost=null;
function openSheet(post){menuPost=post;document.getElementById('sheetBackdrop').classList.add('active');document.getElementById('sheet').classList.add('active');}
function closeSheet(){document.getElementById('sheetBackdrop').classList.remove('active');document.getElementById('sheet').classList.remove('active');menuPost=null;}
function copyText(t){function fb(){var ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');showToast('Link copied 🔗');}catch(e){showToast('Copy not allowed');}ta.remove();}if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){showToast('Link copied 🔗');}).catch(fb);}else{fb();}}
function sheetCopy(){var pid=menuPost?menuPost.id:'post';copyText('https://hmfbook.app/p/'+pid);closeSheet();}
function dl(url,name){var a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){a.remove();},100);}
function downloadPost(post){if(!post)return;var img=post.querySelector('img');if(img){dl(img.src,'hmf-photo.png');showToast('Saved to device ⬇️');return;}var vid=post.querySelector('video');if(vid&&vid.src){dl(vid.src,'hmf-video.mp4');showToast('Saved to device ⬇️');return;}var pe=post.querySelector('.post-img');var emoji=pe?pe.textContent.trim().charAt(0):'⭐';if(!emoji)emoji='⭐';var g=['#89f7fe','#66a6ff'];if(pe){if(pe.className.indexOf('p2')>-1){g=['#fddb92','#d1fdff'];}else if(pe.className.indexOf('p3')>-1){g=['#a18cd1','#fbc2eb'];}}var c=document.createElement('canvas');c.width=600;c.height=600;var x=c.getContext('2d');var gr=x.createLinearGradient(0,0,600,600);gr.addColorStop(0,g[0]);gr.addColorStop(1,g[1]);x.fillStyle=gr;x.fillRect(0,0,600,600);x.font='280px serif';x.textAlign='center';x.textBaseline='middle';x.fillText(emoji,300,320);dl(c.toDataURL('image/png'),'hmf-post.png');showToast('Saved to device ⬇️');}
function sheetSave(){if(menuPost){downloadPost(menuPost);}closeSheet();}
function sheetDelete(){if(menuPost){menuPost.remove();showToast('Post deleted 🗑️');}closeSheet();}
function showGame(id){document.getElementById('gameMenu').style.display='none';document.querySelectorAll('.game-panel').forEach(function(p){p.classList.remove('active');});document.getElementById(id).classList.add('active');if(id==='gTTT')resetGame();if(id==='gMem')startMemory();if(id==='gRace')startRace();if(id==='gSnk')startSnooker();if(id==='gLudo')ludoReset();}
function backToGames(){document.querySelectorAll('.game-panel').forEach(function(p){p.classList.remove('active');});var m=document.getElementById('gameMenu');if(m)m.style.display='block';if(raceState.running){clearInterval(raceState.loop);raceState.running=false;}if(snk.timer){clearInterval(snk.timer);snk.timer=null;}}
var board=['','','','','','','','',''];var current='X';var gameOver=false;
function renderBoard(){var c=document.getElementById('ttt');c.innerHTML='';for(var i=0;i<9;i++){(function(i){var d=document.createElement('div');d.className='cell';d.textContent=board[i];d.onclick=function(){playCell(i);};c.appendChild(d);})(i);}}
function playCell(i){if(gameOver||board[i]!=='')return;board[i]=current;renderBoard();var w=checkWin();if(w){gameOver=true;document.getElementById('gameStatus').textContent=(w==='Draw')?'Draw! 🤝':(w+' wins! 🎉');return;}current=(current==='X')?'O':'X';document.getElementById('gameStatus').textContent='Turn: '+current;}
function checkWin(){var lines=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];for(var i=0;i<lines.length;i++){var a=lines[i][0],b=lines[i][1],c=lines[i][2];if(board[a]!==''&&board[a]===board[b]&&board[a]===board[c])return board[a];}return board.indexOf('')===-1?'Draw':null;}
function resetGame(){board=['','','','','','','','',''];current='X';gameOver=false;renderBoard();document.getElementById('gameStatus').textContent='Turn: X';}
renderBoard();
var raceState={running:false,score:0,carX:130,obs:[],loop:null,tick:0};
function startRace(){raceState.running=true;raceState.score=0;raceState.carX=130;raceState.obs=[];raceState.tick=0;document.getElementById('raceOver').style.display='none';clearInterval(raceState.loop);raceState.loop=setInterval(raceStep,40);}
function raceStep(){var cv=document.getElementById('raceCanvas');var cx=cv.getContext('2d');var W=cv.width,H=cv.height;raceState.tick++;cx.fillStyle='#2c3e50';cx.fillRect(0,0,W,H);cx.fillStyle='#7f8c8d';cx.fillRect(0,0,8,H);cx.fillRect(W-8,0,8,H);cx.fillStyle='#fff';for(var i=-1;i<10;i++){cx.fillRect(146,(i*50+(raceState.tick*8)%50),8,26);}if(Math.random()<0.06){raceState.obs.push({x:10+Math.random()*240,y:-70});}for(var j=raceState.obs.length-1;j>=0;j--){var o=raceState.obs[j];o.y+=8;cx.fillStyle='#e74c3c';cx.fillRect(o.x,o.y,40,60);cx.fillStyle='#b03a2e';cx.fillRect(o.x+5,o.y+8,12,16);cx.fillRect(o.x+23,o.y+8,12,16);if(o.y>H){raceState.obs.splice(j,1);raceState.score++;document.getElementById('raceScore').textContent='Score: '+raceState.score;continue;}if(o.y<H-20&&o.y+60>H-80&&o.x<raceState.carX+40&&o.x+40>raceState.carX){raceCrash();return;}}cx.fillStyle='#00d67e';cx.fillRect(raceState.carX,H-80,40,60);cx.fillStyle='#0b3d2a';cx.fillRect(raceState.carX+6,H-72,10,16);cx.fillRect(raceState.carX+24,H-72,10,16);cx.fillStyle='#f1c40f';cx.fillRect(raceState.carX+14,H-14,12,8);}
function raceMove(dir){if(!raceState.running)startRace();raceState.carX+=dir*40;if(raceState.carX<10)raceState.carX=10;if(raceState.carX>250)raceState.carX=250;}
function raceCrash(){clearInterval(raceState.loop);raceState.running=false;document.getElementById('raceOver').style.display='block';}
document.addEventListener('keydown',function(e){if(!raceState.running)return;if(e.key==='ArrowLeft')raceMove(-1);if(e.key==='ArrowRight')raceMove(1);});
var ludo={p:0,c:0,busy:false};
function ludoReset(){ludo.p=0;ludo.c=0;ludo.busy=false;document.getElementById('ludoDice').textContent='🎲';updateLudo();document.getElementById('ludoMsg').textContent='Your turn — Roll!';}
function updateLudo(){document.getElementById('ludoPBar').style.width=Math.min(100,ludo.p/30*100)+'%';document.getElementById('ludoCBar').style.width=Math.min(100,ludo.c/30*100)+'%';document.getElementById('ludoPStep').textContent=ludo.p+'/30';document.getElementById('ludoCStep').textContent=ludo.c+'/30';}
function ludoRoll(){if(ludo.busy)return;ludo.busy=true;var d=1+Math.floor(Math.random()*6);document.getElementById('ludoDice').textContent='🎲 '+d;ludo.p+=d;updateLudo();if(ludo.p>=30){document.getElementById('ludoMsg').textContent='🎉 You win!';return;}document.getElementById('ludoMsg').textContent='Computer turn...';setTimeout(function(){var d2=1+Math.floor(Math.random()*6);document.getElementById('ludoDice').textContent='🎲 '+d2;ludo.c+=d2;updateLudo();if(ludo.c>=30){document.getElementById('ludoMsg').textContent='🤖 Computer wins!';return;}document.getElementById('ludoMsg').textContent='Your turn — Roll!';ludo.busy=false;},1000);}
var snk={balls:[],score:0,timer:null};
function startSnooker(){var cv=document.getElementById('snkCanvas');var H=cv.height;snk.balls=[{x:150,y:H-100,vx:0,vy:0,c:'#fff'},{x:150,y:150,vx:0,vy:0,c:'#e74c3c'},{x:110,y:115,vx:0,vy:0,c:'#f1c40f'},{x:190,y:115,vx:0,vy:0,c:'#3498db'}];snk.score=0;document.getElementById('snkScore').textContent='Potted: 0 / 3';if(snk.timer){clearInterval(snk.timer);snk.timer=null;}drawSnk();}
function drawSnk(){var cv=document.getElementById('snkCanvas');var cx=cv.getContext('2d');var W=cv.width,H=cv.height;cx.fillStyle='#0a5c2e';cx.fillRect(0,0,W,H);cx.strokeStyle='rgba(255,255,255,.25)';cx.strokeRect(10,10,W-20,H-20);var ps=[[15,15],[W-15,15],[15,H-15],[W-15,H-15]];for(var i=0;i<4;i++){cx.fillStyle='#000';cx.beginPath();cx.arc(ps[i][0],ps[i][1],14,0,7);cx.fill();}for(var j=0;j<snk.balls.length;j++){var b=snk.balls[j];cx.fillStyle=b.c;cx.beginPath();cx.arc(b.x,b.y,10,0,7);cx.fill();cx.strokeStyle='rgba(0,0,0,.35)';cx.stroke();}}
function snkLoop(){var cv=document.getElementById('snkCanvas');var W=cv.width,H=cv.height;var moving=false;for(var i=0;i<snk.balls.length;i++){var b=snk.balls[i];b.x+=b.vx;b.y+=b.vy;b.vx*=0.985;b.vy*=0.985;if(Math.abs(b.vx)<0.05&&Math.abs(b.vy)<0.05){b.vx=0;b.vy=0;}else{moving=true;}if(b.x<10){b.x=10;b.vx=Math.abs(b.vx)*0.8;}if(b.x>W-10){b.x=W-10;b.vx=-Math.abs(b.vx)*0.8;}if(b.y<10){b.y=10;b.vy=Math.abs(b.vy)*0.8;}if(b.y>H-10){b.y=H-10;b.vy=-Math.abs(b.vy)*0.8;}var potted=false;var ps=[[15,15],[W-15,15],[15,H-15],[W-15,H-15]];for(var j=0;j<4;j++){var dx=b.x-ps[j][0],dy=b.y-ps[j][1];if(dx*dx+dy*dy<256){if(b.c==='#fff'){b.x=150;b.y=H-100;b.vx=0;b.vy=0;showToast('Oops! White ball 😅');}else{snk.balls.splice(i,1);snk.score++;document.getElementById('snkScore').textContent='Potted: '+snk.score+' / 3';showToast('Potted! 🎉');if(snk.score>=3){setTimeout(function(){showToast('Table cleared! 🏆');},600);}}potted=true;break;}}if(potted){i--;continue;}for(var k=0;k<snk.balls.length;k++){if(k===i)continue;var o=snk.balls[k];var ddx=o.x-b.x,ddy=o.y-b.y;var dist=Math.sqrt(ddx*ddx+ddy*ddy);if(dist<20&&dist>0.001){var nx=ddx/dist,ny=ddy/dist;var rel=(b.vx-o.vx)*nx+(b.vy-o.vy)*ny;if(rel>0){b.vx-=rel*nx;b.vy-=rel*ny;o.vx+=rel*nx;o.vy+=rel*ny;moving=true;}var ov=20-dist;b.x-=nx*ov/2;b.y-=ny*ov/2;o.x+=nx*ov/2;o.y+=ny*ov/2;}}}drawSnk();if(!moving&&snk.timer){clearInterval(snk.timer);snk.timer=null;}}
function snkShoot(dx,dy){var len=Math.sqrt(dx*dx+dy*dy);if(len<12)return;var p=Math.min(14,len*0.08);var w=snk.balls[0];w.vx=-dx/len*p;w.vy=-dy/len*p;if(!snk.timer)snk.timer=setInterval(snkLoop,16);}
(function(){var cv=document.getElementById('snkCanvas');var sx=0,sy=0,on=false;function pos(e){var r=cv.getBoundingClientRect();return {x:(e.clientX-r.left)*cv.width/r.width,y:(e.clientY-r.top)*cv.height/r.height};}cv.addEventListener('mousedown',function(e){var p=pos(e);sx=p.x;sy=p.y;on=true;});window.addEventListener('mouseup',function(e){if(!on)return;on=false;var p=pos(e);snkShoot(p.x-sx,p.y-sy);});cv.addEventListener('touchstart',function(e){var p=pos(e.touches[0]);sx=p.x;sy=p.y;on=true;e.preventDefault();},{passive:false});cv.addEventListener('touchend',function(e){if(!on)return;on=false;var p=pos(e.changedTouches[0]);snkShoot(p.x-sx,p.y-sy);e.preventDefault();},{passive:false});})();
var memEmojis=['🍎','🚗','🐶','🌸','⚽','🎵','⭐','🍕'];
var memOpen=[],memMoves=0,memLock=false;
function startMemory(){var deck=memEmojis.concat(memEmojis).sort(function(){return Math.random()-0.5;});memOpen=[];memMoves=0;memLock=false;var g=document.getElementById('memGrid');g.innerHTML='';for(var i=0;i<16;i++){(function(i){var d=document.createElement('div');d.className='mem-card';d.dataset.val=deck[i];d.textContent='';d.onclick=function(){memFlip(d);};g.appendChild(d);})(i);}document.getElementById('memMoves').textContent='Moves: 0';}
function memFlip(d){if(memLock||d.classList.contains('open')||d.classList.contains('done'))return;d.textContent=d.dataset.val;d.classList.add('open');memOpen.push(d);if(memOpen.length===2){memMoves++;document.getElementById('memMoves').textContent='Moves: '+memMoves;if(memOpen[0].dataset.val===memOpen[1].dataset.val){memOpen[0].classList.add('done');memOpen[1].classList.add('done');memOpen=[];if(document.querySelectorAll('.mem-card.done').length===16){showToast('You won! 🎉');}}else{memLock=true;var a=memOpen[0],b2=memOpen[1];setTimeout(function(){a.textContent='';a.classList.remove('open');b2.textContent='';b2.classList.remove('open');memOpen=[];memLock=false;},700);}}}
function rpsPlay(ch){var em={rock:'✊',paper:'✋',scissors:'✌️'};var opts=['rock','paper','scissors'];var cc=opts[Math.floor(Math.random()*3)];document.getElementById('rpsYou').textContent=em[ch];document.getElementById('rpsComp').textContent=em[cc];var res;if(ch===cc){res='Draw! 🤝';}else if((ch==='rock'&&cc==='scissors')||(ch==='paper'&&cc==='rock')||(ch==='scissors'&&cc==='paper')){res='You win! 🎉';}else{res='Computer wins! 🤖';}document.getElementById('rpsResult').textContent=res;}
tryAutoLogin();
</script>
</body>
</html>
"""

components.html(APP_HTML, height=880, scrolling=True)
