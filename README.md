<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HMF Book</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; font-family:'Poppins',sans-serif; }
body { background:#eef2f5; min-height:100vh; }
.screen { display:none; min-height:100vh; }
.screen.active { display:block; }

/* ================= SPLASH ================= */
#splash {
  background:linear-gradient(135deg,#00a05a 0%,#00c47e 50%,#00d68f 100%);
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  position:relative; overflow:hidden; text-align:center;
}
.deco { position:absolute; opacity:.12; }
.deco.tri1 { top:12%; left:8%; width:0; height:0; border-left:40px solid transparent; border-right:40px solid transparent; border-bottom:70px solid #fff; transform:rotate(20deg); }
.deco.tri2 { top:20%; right:10%; width:0; height:0; border-left:30px solid transparent; border-right:30px solid transparent; border-bottom:55px solid #fff; transform:rotate(-30deg); }
.deco.tri3 { bottom:25%; left:12%; width:0; height:0; border-left:25px solid transparent; border-right:25px solid transparent; border-bottom:45px solid #fff; transform:rotate(45deg); }
.deco.tri4 { bottom:15%; right:15%; width:0; height:0; border-left:35px solid transparent; border-right:35px solid transparent; border-bottom:60px solid #fff; transform:rotate(-15deg); }
.deco.circle1 { top:40%; right:5%; width:100px; height:100px; border:2px solid #fff; border-radius:50%; }
.deco.circle2 { bottom:35%; left:5%; width:70px; height:70px; border:2px solid #fff; border-radius:50%; }
.splash-logo { font-size:90px; font-weight:800; color:#fff; letter-spacing:2px; z-index:2; }
.splash-sub { font-size:34px; font-weight:600; color:#fff; margin-top:-5px; z-index:2; }
.btn-get {
  margin-top:120px; background:#fff; color:#00b86e; border:none; padding:16px 70px;
  font-size:22px; font-weight:600; border-radius:50px; cursor:pointer; z-index:2;
  box-shadow:0 8px 20px rgba(0,0,0,.15); transition:.3s;
}
.btn-get:hover { transform:scale(1.05); }

/* ================= AUTH (Sign up / Login) ================= */
.auth { display:flex; flex-direction:column; }
.auth-top {
  background:linear-gradient(135deg,#00a05a 0%,#00c47e 50%,#00d68f 100%);
  min-height:32vh; display:flex; justify-content:center; align-items:center;
  position:relative; overflow:hidden; border-radius:0 0 0 0;
}
.auth-logo { font-size:80px; font-weight:800; color:#fff; z-index:2; }
.auth-card {
  background:#fff; border-radius:35px 35px 0 0; margin-top:-45px; padding:35px 25px 40px;
  flex:1; max-width:480px; width:100%; margin-left:auto; margin-right:auto;
}
.auth-card h2 { font-size:32px; color:#222; margin-bottom:25px; }
.input-box { display:flex; align-items:center; border:1px solid #dfe3e8; border-radius:14px; padding:15px 18px; margin-bottom:18px; }
.input-box svg { width:22px; height:22px; stroke:#9aa4af; flex-shrink:0; }
.input-box input { border:none; outline:none; flex:1; margin-left:12px; font-size:16px; color:#333; background:transparent; }
.input-box input::placeholder { color:#9aa4af; }
.eye-btn { background:none; border:none; cursor:pointer; display:flex; }
.btn-main {
  width:100%; background:#00b86e; color:#fff; border:none; padding:16px;
  font-size:20px; font-weight:600; border-radius:50px; cursor:pointer; transition:.3s; margin-top:5px;
}
.btn-main:hover { background:#00a05a; }
.divider { display:flex; align-items:center; color:#6b7480; font-size:14px; margin:25px 0 20px; }
.divider::before, .divider::after { content:""; flex:1; height:1px; background:#e3e7ec; }
.divider span { padding:0 12px; }
.social-btns { display:flex; justify-content:center; gap:25px; }
.soc { width:52px; height:52px; border-radius:50%; border:none; cursor:pointer; display:flex; justify-content:center; align-items:center; font-size:22px; font-weight:700; color:#fff; transition:.3s; }
.soc:hover { transform:scale(1.1); }
.soc.google { background:#fff; border:1px solid #e3e7ec; color:#ea4335; }
.soc.snap { background:#fffc00; color:#fff; }
.soc.fb { background:#1877f2; }
.switch-auth { text-align:center; margin-top:25px; font-size:15px; color:#6b7480; }
.switch-auth a { color:#00b86e; font-weight:600; text-decoration:none; cursor:pointer; }
.pass-note { font-size:12px; color:#9aa4af; margin-top:-10px; margin-bottom:15px; padding-left:5px; }
.error-msg { color:#e53935; font-size:14px; margin-bottom:12px; display:none; }
.success-msg { color:#00b86e; font-size:14px; margin-bottom:12px; display:none; }

/* ================= MAIN APP ================= */
#mainApp { display:none; }
#mainApp.active { display:block; }
.navbar {
  background:#fff; display:flex; align-items:center; gap:15px; padding:8px 16px;
  position:sticky; top:0; z-index:100; box-shadow:0 1px 4px rgba(0,0,0,.1);
}
.nav-logo { font-size:30px; font-weight:800; color:#00b86e; }
.nav-search { flex:1; max-width:280px; display:flex; align-items:center; background:#eef2f5; border-radius:50px; padding:9px 16px; }
.nav-search input { border:none; outline:none; background:transparent; margin-left:10px; font-size:14px; width:100%; }
.nav-icons { margin-left:auto; display:flex; gap:10px; }
.nav-icon {
  width:42px; height:42px; border-radius:50%; background:#eef2f5; border:none;
  display:flex; justify-content:center; align-items:center; cursor:pointer; font-size:18px; position:relative;
}
.nav-icon .badge { position:absolute; top:-2px; right:-2px; background:#e53935; color:#fff; font-size:10px; padding:1px 5px; border-radius:10px; }
.nav-user { display:flex; align-items:center; gap:8px; cursor:pointer; }
.avatar { width:38px; height:38px; border-radius:50%; background:linear-gradient(135deg,#00b86e,#00d68f); color:#fff; display:flex; justify-content:center; align-items:center; font-weight:700; }
.layout { display:flex; max-width:1200px; margin:0 auto; padding:20px 15px; gap:20px; }
.sidebar { width:250px; flex-shrink:0; }
.side-item { display:flex; align-items:center; gap:12px; padding:10px 12px; border-radius:10px; cursor:pointer; font-size:15px; color:#333; font-weight:500; }
.side-item:hover { background:#e4e9ee; }
.side-item .ico { width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg,#00b86e,#00d68f); display:flex; justify-content:center; align-items:center; font-size:17px; }
.feed { flex:1; max-width:560px; margin:0 auto; }
.create-post { background:#fff; border-radius:14px; padding:16px; margin-bottom:18px; box-shadow:0 1px 3px rgba(0,0,0,.08); }
.cp-top { display:flex; align-items:center; gap:10px; }
.cp-top input { flex:1; border:none; outline:none; background:#eef2f5; border-radius:50px; padding:11px 18px; font-size:15px; }
.cp-actions { display:flex; justify-content:space-around; margin-top:12px; border-top:1px solid #eef2f5; padding-top:10px; }
.cp-btn { background:none; border:none; cursor:pointer; font-size:14px; color:#65676b; font-weight:500; padding:6px 12px; border-radius:8px; }
.cp-btn:hover { background:#eef2f5; }
.post { background:#fff; border-radius:14px; margin-bottom:18px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.08); }
.post-head { display:flex; align-items:center; gap:10px; padding:14px 16px 6px; }
.post-head .name { font-weight:600; font-size:15px; }
.post-head .time { font-size:12px; color:#8a8d91; }
.post-text { padding:6px 16px 12px; font-size:15px; color:#1c1e21; }
.post-img { width:100%; max-height:350px; object-fit:cover; display:block; background:#d8e0e6; }
.post-stats { display:flex; justify-content:space-between; padding:10px 16px; font-size:13px; color:#65676b; border-bottom:1px solid #eef2f5; }
.post-actions { display:flex; }
.pa-btn { flex:1; background:none; border:none; padding:10px; font-size:14px; font-weight:600; color:#65676b; cursor:pointer; }
.pa-btn:hover { background:#f0f2f5; }
.pa-btn.liked { color:#00b86e; }
.comments { padding:8px 16px 14px; display:none; }
.comment { background:#f0f2f5; border-radius:16px; padding:8px 12px; margin-bottom:6px; font-size:14px; }
.comment b { font-size:13px; display:block; }
.comment-input { display:flex; gap:8px; margin-top:8px; }
.comment-input input { flex:1; border:none; outline:none; background:#f0f2f5; border-radius:50px; padding:9px 14px; font-size:14px; }
.comment-input button { background:#00b86e; color:#fff; border:none; border-radius:50px; padding:0 18px; cursor:pointer; font-weight:600; }
.online-dot { width:10px; height:10px; background:#31a24c; border-radius:50%; border:2px solid #fff; }
.contact { display:flex; align-items:center; gap:10px; padding:8px 10px; border-radius:10px; cursor:pointer; font-size:14px; font-weight:500; }
.contact:hover { background:#e4e9ee; }
.side-title { font-size:16px; font-weight:600; color:#65676b; padding:5px 10px; }
.logout-btn { margin-top:15px; width:100%; background:#eef2f5; color:#e53935; border:none; padding:11px; border-radius:10px; font-weight:600; cursor:pointer; }

/* ================= RESPONSIVE ================= */
@media (max-width: 900px) {
  .sidebar.right { display:none; }
}
@media (max-width: 640px) {
  .sidebar.left { display:none; }
  .splash-logo { font-size:64px; }
  .splash-sub { font-size:24px; }
  .auth-logo { font-size:56px; }
  .auth-top { min-height:26vh; }
  .auth-card h2 { font-size:26px; }
  .nav-search { display:none; }
  .nav-user span { display:none; }
}
</style>
</head>
<body>

<!-- ============ SPLASH SCREEN ============ -->
<div id="splash" class="screen active">
  <div class="deco tri1"></div><div class="deco tri2"></div>
  <div class="deco tri3"></div><div class="deco tri4"></div>
  <div class="deco circle1"></div><div class="deco circle2"></div>
  <div class="splash-logo">HMF</div>
  <div class="splash-sub">HMF book</div>
  <button class="btn-get" onclick="showScreen('signup')">Get Started</button>
</div>

<!-- ============ SIGN UP ============ -->
<div id="signup" class="screen auth">
  <div class="auth-top">
    <div class="deco tri1"></div><div class="deco tri2"></div><div class="deco circle1"></div>
    <div class="auth-logo">HMF</div>
  </div>
  <div class="auth-card">
    <h2>Create Account</h2>
    <div class="success-msg" id="signupSuccess"></div>
    <div class="error-msg" id="signupError"></div>
    <div class="input-box">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>
      <input type="text" id="suName" placeholder="Username">
    </div>
    <div class="input-box">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
      <input type="email" id="suEmail" placeholder="Email">
    </div>
    <div class="input-box">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/></svg>
      <input type="password" id="suPass" placeholder="Password">
      <button class="eye-btn" onclick="togglePass('suPass',this)">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" width="22" height="22" stroke="#9aa4af"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>
    </div>
    <div class="pass-note">Password must be at least 6 characters</div>
    <button class="btn-main" onclick="signup()">Sign Up</button>
    <div class="divider"><span>Or continue with</span></div>
    <div class="social-btns">
      <button class="soc google">G</button>
      <button class="soc snap">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M12 2c3 0 5 2.2 5 5v2.5c.8.3 1.8-.5 2.3 0 .5.6-.8 1.4-1.7 1.9.9 2 2.4 3 4.4 3.4-.3 1.2-2.3 1.5-3.2 1.7-.2.6 0 1.4-.6 1.5-.8.2-1.9-.3-3 .2-1 .5-1.9 1.8-3.2 1.8s-2.2-1.3-3.2-1.8c-1.1-.5-2.2 0-3-.2-.6-.1-.4-.9-.6-1.5-.9-.2-2.9-.5-3.2-1.7 2-.4 3.5-1.4 4.4-3.4-.9-.5-2.2-1.3-1.7-1.9.5-.5 1.5.3 2.3 0V7c0-2.8 2-5 5-5z"/></svg>
      </button>
      <button class="soc fb">f</button>
    </div>
    <div class="switch-auth">Already have an account? <a onclick="showScreen('login')">Log In</a></div>
  </div>
</div>

<!-- ============ LOGIN ============ -->
<div id="login" class="screen auth">
  <div class="auth-top">
    <div class="deco tri1"></div><div class="deco tri2"></div><div class="deco circle1"></div>
    <div class="auth-logo">HMF</div>
  </div>
  <div class="auth-card">
    <h2>Log In</h2>
    <div class="error-msg" id="loginError"></div>
    <div class="input-box">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>
      <input type="text" id="liEmail" placeholder="Email or Username">
    </div>
    <div class="input-box">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/></svg>
      <input type="password" id="liPass" placeholder="Password">
      <button class="eye-btn" onclick="togglePass('liPass',this)">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" width="22" height="22" stroke="#9aa4af"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>
      </button>
    </div>
    <button class="btn-main" onclick="login()">Log In</button>
    <div class="divider"><span>Or continue with</span></div>
    <div class="social-btns">
      <button class="soc google">G</button>
      <button class="soc snap">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="#fff"><path d="M12 2c3 0 5 2.2 5 5v2.5c.8.3 1.8-.5 2.3 0 .5.6-.8 1.4-1.7 1.9.9 2 2.4 3 4.4 3.4-.3 1.2-2.3 1.5-3.2 1.7-.2.6 0 1.4-.6 1.5-.8.2-1.9-.3-3 .2-1 .5-1.9 1.8-3.2 1.8s-2.2-1.3-3.2-1.8c-1.1-.5-2.2 0-3-.2-.6-.1-.4-.9-.6-1.5-.9-.2-2.9-.5-3.2-1.7 2-.4 3.5-1.4 4.4-3.4-.9-.5-2.2-1.3-1.7-1.9.5-.5 1.5.3 2.3 0V7c0-2.8 2-5 5-5z"/></svg>
      </button>
      <button class="soc fb">f</button>
    </div>
    <div class="switch-auth">Don't have an account? <a onclick="showScreen('signup')">Sign Up</a></div>
  </div>
</div>

<!-- ============ MAIN APP ============ -->
<div id="mainApp" class="screen">
  <nav class="navbar">
    <div class="nav-logo">HMF</div>
    <div class="nav-search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#65676b" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input placeholder="Search HMF">
    </div>
    <div class="nav-icons">
      <button class="nav-icon">🔔<span class="badge">3</span></button>
      <button class="nav-icon">💬<span class="badge">5</span></button>
      <div class="nav-user" onclick="null">
        <div class="avatar" id="navAvatar">H</div><span id="navName" style="font-weight:600;font-size:14px">User</span>
      </div>
    </div>
  </nav>

  <div class="layout">
    <!-- LEFT SIDEBAR -->
    <div class="sidebar left">
      <div class="side-item"><div class="ico">👤</div><span id="sideName">My Profile</span></div>
      <div class="side-item"><div class="ico">👥</div>Friends</div>
      <div class="side-item"><div class="ico">📦</div>Groups</div>
      <div class="side-item"><div class="ico">🎬</div>Watch</div>
      <div class="side-item"><div class="ico">🗓️</div>Events</div>
      <div class="side-item"><div class="ico">💾</div>Saved</div>
      <button class="logout-btn" onclick="logout()">Log Out</button>
    </div>

    <!-- FEED -->
    <div class="feed">
      <div class="create-post">
        <div class="cp-top">
          <div class="avatar" id="cpAvatar">H</div>
          <input id="postInput" placeholder="What's on your mind?" onkeydown="if(event.key==='Enter')createPost()">
        </div>
        <div class="cp-actions">
          <button class="cp-btn" onclick="createPost()">📷 Photo</button>
          <button class="cp-btn" onclick="createPost()">🏷️ Tag</button>
          <button class="cp-btn" onclick="createPost()">😊 Feeling</button>
        </div>
      </div>
      <div id="feedArea"></div>
    </div>

    <!-- RIGHT SIDEBAR -->
    <div class="sidebar right">
      <div class="side-title">Sponsored</div>
      <div class="side-item"><div class="ico">🛍️</div><span style="font-size:13px">Shop Now<br><small style="color:#8a8d91">hmfshop.com</small></span></div>
      <div class="side-title" style="margin-top:10px">Contacts</div>
      <div class="contact"><div class="avatar" style="width:34px;height:34px;font-size:13px">A</div>Ahmed<div class="online-dot" style="margin-left:auto"></div></div>
      <div class="contact"><div class="avatar" style="width:34px;height:34px;font-size:13px">S</div>Sara<div class="online-dot" style="margin-left:auto"></div></div>
      <div class="contact"><div class="avatar" style="width:34px;height:34px;font-size:13px">B</div>Bilal</div>
      <div class="contact"><div class="avatar" style="width:34px;height:34px;font-size:13px">F</div>Fatima<div class="online-dot" style="margin-left:auto"></div></div>
    </div>
  </div>
</div>

<script>
/* ---------- Screen Switch ---------- */
function showScreen(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

/* ---------- Password Eye Toggle ---------- */
function togglePass(id,btn){
  const inp=document.getElementById(id);
  if(inp.type==='password'){ inp.type='text'; btn.style.opacity='.5'; }
  else{ inp.type='password'; btn.style.opacity='1'; }
}

/* ---------- Sign Up ---------- */
function signup(){
  const name=document.getElementById('suName').value.trim();
  const email=document.getElementById('suEmail').value.trim();
  const pass=document.getElementById('suPass').value;
  const err=document.getElementById('signupError');
  const ok=document.getElementById('signupSuccess');
  err.style.display='none'; ok.style.display='none';

  if(!name||!email||!pass){ err.textContent='⚠️ Please fill all fields'; err.style.display='block'; return; }
  if(pass.length<6){ err.textContent='⚠️ Password must be at least 6 characters'; err.style.display='block'; return; }

  const users=JSON.parse(localStorage.getItem('hmf_users')||'[]');
  if(users.find(u=>u.email===email)){ err.textContent='⚠️ This email is already registered'; err.style.display='block'; return; }

  users.push({name,email,pass});
  localStorage.setItem('hmf_users',JSON.stringify(users));
  localStorage.setItem('hmf_current',JSON.stringify({name,email}));
  startApp(name);
}

/* ---------- Login ---------- */
function login(){
  const id=document.getElementById('liEmail').value.trim();
  const pass=document.getElementById('liPass').value;
  const err=document.getElementById('loginError');
  err.style.display='none';

  const users=JSON.parse(localStorage.getItem('hmf_users')||'[]');
  const user=users.find(u=>(u.email===id||u.name===id)&&u.pass===pass);
  if(!user){ err.textContent='⚠️ Invalid email/username or password'; err.style.display='block'; return; }

  localStorage.setItem('hmf_current',JSON.stringify({name:user.name,email:user.email}));
  startApp(user.name);
}

/* ---------- Start Main App ---------- */
function startApp(name){
  document.getElementById('navName').textContent=name;
  document.getElementById('sideName').textContent=name+"'s Profile";
  ['navAvatar','cpAvatar'].forEach(i=>document.getElementById(i).textContent=name[0].toUpperCase());
  showScreen('mainApp');
  loadFeed();
}

/* ---------- Logout ---------- */
function logout(){
  localStorage.removeItem('hmf_current');
  showScreen('splash');
}

/* ---------- Posts ---------- */
const demoPosts=[
  {name:'Ahmed Khan',time:'2 hrs',text:'HMF book is amazing! 🔥',likes:24,comments:[{n:'Sara',t:'Totally agree!'}]},
  {name:'Sara Ali',time:'5 hrs',text:'Good morning everyone ☀️ Have a great day!',likes:56,comments:[]},
  {name:'Bilal Ahmed',time:'1 day',text:'Just joined HMF book. Loving it so far!',likes:12,comments:[{n:'Fatima',t:'Welcome! 👋'}]}
];

function loadFeed(){
  const posts=JSON.parse(localStorage.getItem('hmf_posts')||'null')||demoPosts;
  renderPosts(posts);
}

function savePosts(posts){ localStorage.setItem('hmf_posts',JSON.stringify(posts)); }

function renderPosts(posts){
  const area=document.getElementById('feedArea');
  area.innerHTML='';
  posts.forEach((p,idx)=>{
    const liked=(JSON.parse(localStorage.getItem('hmf_liked')||'[]')).includes(idx);
    const div=document.createElement('div');
    div.className='post';
    div.innerHTML=`
      <div class="post-head">
        <div class="avatar">${p.name[0].toUpperCase()}</div>
        <div><div class="name">${p.name}</div><div class="time">${p.time}</div></div>
      </div>
      <div class="post-text">${p.text}</div>
      <div class="post-stats"><span>👍❤️ ${p.likes}</span><span>${p.comments.length} comments</span></div>
      <div class="post-actions">
        <button class="pa-btn ${liked?'liked':''}" onclick="likePost(${idx})">👍 Like</button>
        <button class="pa-btn" onclick="toggleComments(${idx})">💬 Comment</button>
        <button class="pa-btn">↗ Share</button>
      </div>
      <div class="comments" id="cmts${idx}">
        ${p.comments.map(c=>`<div class="comment"><b>${c.n}</b>${c.t}</div>`).join('')}
        <div class="comment-input">
          <input placeholder="Write a comment..." onkeydown="if(event.key==='Enter')addComment(${idx},this)">
          <button onclick="addComment(${idx},this.previousElementSibling)">Send</button>
        </div>
      </div>`;
    area.appendChild(div);
  });
}

function createPost(){
  const input=document.getElementById('postInput');
  const text=input.value.trim();
  if(!text) return alert('Please write something first!');
  const cur=JSON.parse(localStorage.getItem('hmf_current'));
  const posts=JSON.parse(localStorage.getItem('hmf_posts')||'null')||demoPosts;
  posts.unshift({name:cur.name,time:'Just now',text:text,likes:0,comments:[]});
  savePosts(posts);
  input.value='';
  renderPosts(posts);
}

function likePost(idx){
  const posts=JSON.parse(localStorage.getItem('hmf_posts')||'null')||demoPosts;
  let liked=JSON.parse(localStorage.getItem('hmf_liked')||'[]');
  if(liked.includes(idx)){ liked=liked.filter(i=>i!==idx); posts[idx].likes--; }
  else{ liked.push(idx); posts[idx].likes++; }
  localStorage.setItem('hmf_liked',JSON.stringify(liked));
  savePosts(posts);
  renderPosts(posts);
}

function toggleComments(idx){
  const c=document.getElementById('cmts'+idx);
  c.style.display=c.style.display==='block'?'none':'block';
}

function addComment(idx,inp){
  const text=inp.value.trim();
  if(!text) return;
  const cur=JSON.parse(localStorage.getItem('hmf_current'));
  const posts=JSON.parse(localStorage.getItem('hmf_posts')||'null')||demoPosts;
  posts[idx].comments.push({n:cur.name,t:text});
  savePosts(posts);
  renderPosts(posts);
  document.getElementById('cmts'+idx).style.display='block';
}

/* ---------- Auto login if already logged in ---------- */
window.onload=function(){
  const cur=localStorage.getItem('hmf_current');
  if(cur){ startApp(JSON.parse(cur).name); }
};
</script>
</body>
</html>
