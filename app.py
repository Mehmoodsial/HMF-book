<!DOCTYPE html>
<html lang="ur">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SnapReel 📱</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',system-ui,sans-serif}
body{background:#0b0b0f;color:#fff;max-width:480px;margin:0 auto;min-height:100vh}
button{cursor:pointer;border:none;background:none;color:inherit}

/* Header */
header{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;position:sticky;top:0;background:rgba(11,11,15,.95);z-index:50}
header h1{font-size:22px;background:linear-gradient(90deg,#ffd60a,#ff006e,#8338ec);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800}

/* Stories (Snapchat style) */
.stories{display:flex;gap:14px;overflow-x:auto;padding:10px 16px;scrollbar-width:none}
.stories::-webkit-scrollbar{display:none}
.story{display:flex;flex-direction:column;align-items:center;gap:4px;min-width:64px;cursor:pointer}
.story .ring{width:62px;height:62px;border-radius:50%;padding:3px;background:conic-gradient(#ffd60a,#ff006e,#8338ec,#ffd60a)}
.story.seen .ring{background:#333}
.story .ring .inner{width:100%;height:100%;border-radius:50%;background:#1a1a24;display:flex;align-items:center;justify-content:center;font-size:28px}
.story span{font-size:11px;color:#aaa;max-width:64px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

/* Feed */
#feed{padding:0 0 80px}
.post{margin:16px;background:#15151d;border-radius:16px;overflow:hidden}
.post-head{display:flex;align-items:center;gap:10px;padding:10px 12px}
.post-head .avatar{width:38px;height:38px;border-radius:50%;background:#2a2a38;display:flex;align-items:center;justify-content:center;font-size:20px}
.post-head b{font-size:14px}
.post-head small{display:block;color:#888;font-size:11px}
.post video{width:100%;max-height:420px;object-fit:cover;background:#000;display:block}
.post-actions{display:flex;gap:18px;padding:10px 12px;font-size:20px}
.post-caption{padding:0 12px 12px;font-size:13px;color:#ccc}

/* Bottom Nav */
.bottom-nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:480px;display:flex;justify-content:space-around;background:#12121a;border-top:1px solid #222;padding:8px 0;z-index:60}
.bottom-nav button{font-size:24px;padding:6px 14px;border-radius:12px}
.bottom-nav button.active{background:#23233a}

/* Screens */
.screen{position:fixed;inset:0;max-width:480px;margin:0 auto;background:#0b0b0f;z-index:70;display:none;flex-direction:column}
.screen.open{display:flex}
.screen-head{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #222;font-weight:700}
.screen-head .back{font-size:22px;cursor:pointer}

/* Reels */
.reels-wrap{flex:1;overflow-y:auto;scroll-snap-type:y mandatory}
.reel{height:100%;scroll-snap-align:start;position:relative;background:#000;overflow:hidden}
.reel video{width:100%;height:100%;object-fit:cover}
.reel iframe{width:100%;height:100%;border:none;pointer-events:none}
.reel .tap{position:absolute;inset:0;z-index:1}
.reel-overlay{position:absolute;bottom:70px;left:12px;right:70px;z-index:2;text-shadow:0 1px 4px #000;pointer-events:none}
.yt-badge{display:inline-block;background:#f00;color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;margin-bottom:6px}
.reel-overlay b{font-size:14px}
.reel-overlay p{font-size:12px;color:#ddd;margin-top:3px}
.reel-side{position:absolute;right:10px;bottom:80px;z-index:3;display:flex;flex-direction:column;gap:16px;align-items:center}
.reel-side button{font-size:24px;filter:drop-shadow(0 1px 3px #000)}
.reel-side small{font-size:10px;display:block;text-align:center;color:#eee}

/* Chat */
.chat-list{flex:1;overflow-y:auto}
.chat-item{display:flex;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid #1c1c28;cursor:pointer}
.chat-item:hover{background:#15151d}
.chat-item .avatar{width:48px;height:48px;border-radius:50%;background:#2a2a38;display:flex;align-items:center;justify-content:center;font-size:24px}
.chat-item .info{flex:1;min-width:0}
.chat-item b{font-size:14px}
.chat-item small{display:block;color:#888;font-size:12px}
.chat-msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:75%;padding:9px 13px;border-radius:16px;font-size:14px}
.msg.me{align-self:flex-end;background:linear-gradient(135deg,#8338ec,#ff006e);border-bottom-right-radius:4px}
.msg.them{align-self:flex-start;background:#23233a;border-bottom-left-radius:4px}
.chat-input{display:flex;gap:8px;padding:10px 12px;border-top:1px solid #222}
.chat-input input{flex:1;background:#1c1c28;border:none;border-radius:20px;padding:11px 15px;color:#fff;font-size:14px;outline:none}
.chat-input button{font-size:22px;padding:0 10px}

/* Profile */
.profile-head{display:flex;align-items:center;gap:18px;padding:20px 16px}
.profile-head .avatar{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#8338ec,#ff006e);display:flex;align-items:center;justify-content:center;font-size:38px}
.stats{display:flex;flex:1;justify-content:space-around;text-align:center}
.stats b{display:block;font-size:17px}
.stats span{font-size:11px;color:#999}
.profile-tabs{display:flex;border-bottom:1px solid #222;padding:0 12px}
.profile-tabs button{padding:11px 20px;font-size:14px;color:#777;border-bottom:2px solid transparent}
.profile-tabs button.active{color:#fff;border-color:#ff006e}
.video-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;padding:2px}
.video-grid .tile{aspect-ratio:9/14;background:#15151d;border-radius:6px;overflow:hidden;cursor:pointer}
.video-grid .tile video{width:100%;height:100%;object-fit:cover}
.video-grid .tile.empty{display:flex;align-items:center;justify-content:center;color:#444;font-size:24px}

/* Upload Modal */
.modal{position:fixed;inset:0;background:rgba(0,0,0,.8);z-index:90;display:none;align-items:flex-end}
.modal.open{display:flex}
.modal-box{background:#17171f;width:100%;max-width:480px;border-radius:20px 20px 0 0;padding:18px 16px 26px;margin:0 auto}
.modal-box h3{margin-bottom:12px}
.modal-box input[type=text]{width:100%;background:#23233a;border:none;border-radius:10px;padding:12px;color:#fff;margin-bottom:12px;font-size:14px;outline:none}
.pick-btn{display:block;width:100%;padding:13px;border-radius:10px;background:#23233a;font-size:14px;margin-bottom:8px;text-align:center;cursor:pointer}
.publish-btn{display:block;width:100%;padding:13px;border-radius:10px;background:linear-gradient(90deg,#8338ec,#ff006e);font-weight:700;font-size:14px;margin-bottom:8px}
.preview{width:100%;max-height:260px;border-radius:12px;background:#000;margin-bottom:12px;display:none;object-fit:cover}

/* Story Viewer */
.story-viewer{position:fixed;inset:0;background:#000;z-index:100;display:none;flex-direction:column}
.story-viewer.open{display:flex}
.story-viewer .bar{height:3px;background:#444;margin:10px 10px 0;border-radius:3px;overflow:hidden}
.story-viewer .bar i{display:block;height:100%;width:0;background:#fff}
.story-viewer .bar i.go{animation:prog 5s linear forwards}
@keyframes prog{to{width:100%}}
.story-viewer .top{display:flex;align-items:center;gap:10px;padding:12px}
.story-viewer .top .avatar{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;font-size:18px}
.story-viewer .content{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative}
.story-viewer .content .big{font-size:120px}
.story-viewer .content img{max-width:100%;max-height:100%;position:absolute;inset:0}
.story-viewer .nav-l,.story-viewer .nav-r{position:absolute;top:0;bottom:0;width:35%;z-index:5}
.story-viewer .nav-l{left:0}
.story-viewer .nav-r{right:0}
.story-close{position:absolute;top:12px;right:14px;font-size:24px;z-index:6}
</style>
</head>
<body>

<header>
  <h1>SnapReel</h1>
  <span style="font-size:22px">👻</span>
</header>

<!-- Stories Bar -->
<div class="stories" id="storiesBar"></div>

<!-- Feed -->
<main id="feed"></main>

<!-- Bottom Navigation -->
<nav class="bottom-nav">
  <button id="nav-home" class="active" onclick="showScreen('home')">🏠</button>
  <button id="nav-reels" onclick="showScreen('reels')">🎬</button>
  <button onclick="openUpload()">➕</button>
  <button id="nav-chat" onclick="showScreen('chat')">💬</button>
  <button id="nav-profile" onclick="showScreen('profile')">👤</button>
</nav>

<!-- REELS SCREEN -->
<section id="screen-reels" class="screen">
  <div class="screen-head"><span class="back" onclick="closeScreen('reels')">←</span> Reels
    <span style="margin-left:auto"><span class="yt-badge">▶ YouTube</span></span>
  </div>
  <div class="reels-wrap" id="reelsWrap"></div>
</section>

<!-- CHAT SCREEN -->
<section id="screen-chat" class="screen">
  <div class="screen-head" id="chatHead"><span class="back" onclick="closeScreen('chat')">←</span> Messages</div>
  <div class="chat-list" id="chatList"></div>
  <div class="chat-msgs" id="chatMsgs" style="display:none"></div>
  <div class="chat-input" id="chatInputBar" style="display:none">
    <input id="msgInput" placeholder="Message likhein..." onkeydown="if(event.key==='Enter')sendMsg()">
    <button onclick="sendMsg()">➤</button>
  </div>
</section>

<!-- PROFILE SCREEN -->
<section id="screen-profile" class="screen">
  <div class="screen-head"><span class="back" onclick="closeScreen('profile')">←</span> Profile</div>
  <div class="profile-head">
    <div class="avatar">🙂</div>
    <div class="stats">
      <div><b id="statPosts">0</b><span>Videos</span></div>
      <div><b>1.2K</b><span>Followers</span></div>
      <div><b>348</b><span>Following</span></div>
    </div>
  </div>
  <div class="profile-tabs"><button class="active">📹 Videos</button></div>
  <div class="video-grid" id="videoGrid"></div>
</section>

<!-- UPLOAD MODAL -->
<div class="modal" id="uploadModal">
  <div class="modal-box">
    <h3>➕ Video Upload Karein</h3>
    <video id="preview" class="preview" controls muted loop playsinline></video>
    <label class="pick-btn">📁 Video choose karein
      <input type="file" id="videoFile" accept="video/*" hidden onchange="previewVideo(this)">
    </label>
    <input type="text" id="videoCaption" placeholder="Caption likhein...">
    <button class="publish-btn" onclick="publish('reel')">🎬 Reels par daalein</button>
    <button class="publish-btn" onclick="publish('profile')">👤 Profile par daalein</button>
    <button style="width:100%;color:#888;padding:8px" onclick="closeUpload()">Cancel</button>
  </div>
</div>

<!-- STORY VIEWER -->
<div class="story-viewer" id="storyViewer">
  <div class="bar"><i id="storyBar"></i></div>
  <div class="top">
    <div class="avatar" id="svAvatar">👻</div>
    <b id="svName"></b>
    <button class="story-close" onclick="closeStory()">✕</button>
  </div>
  <div class="content" id="svContent">
    <div class="nav-l" onclick="prevStory()"></div>
    <div class="nav-r" onclick="nextStory()"></div>
  </div>
</div>
<input type="file" id="snapFile" accept="image/*" capture="environment" hidden onchange="addMySnap(this)">

<script>
/* ================= DATA ================= */
let stories = [
  {name:'Aapki Story', emoji:'➕', mine:true},
  {name:'Ali',    emoji:'🧑', seen:false, bg:'linear-gradient(135deg,#ff006e,#8338ec)', text:'Snap 👻'},
  {name:'Sara',   emoji:'👧', seen:false, bg:'linear-gradient(135deg,#ffd60a,#ff7b00)', text:'Good morning ☀️'},
  {name:'Bilal',  emoji:'🧔', seen:false, bg:'linear-gradient(135deg,#00b4d8,#0077b6)', text:'Cricket 🏏'},
  {name:'Ayesha', emoji:'👩', seen:true,  bg:'linear-gradient(135deg,#80ffdb,#48cae4)', text:'Coffee ☕'},
];

const feedPosts = [
  {user:'Ali',  avatar:'🧑', time:'2 ghante', video:'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4', caption:'Mera naya video! 🎉'},
  {user:'Sara', avatar:'👧', time:'5 ghante', video:'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4', caption:'Road trip vibes 🚗'},
];

/* Reels: YouTube videos + apni videos */
let reels = [
  {type:'yt', id:'dQw4w9WgXcQ', user:'YouTube', caption:'Classic! 😄', likes:'1.4B'},
  {type:'video', src:'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4', user:'Bilal', caption:'Nature 🌿', likes:'12K'},
  {type:'yt', id:'kJQP7kiw5Fk', user:'YouTube', caption:'Top song 🎶', likes:'8B'},
  {type:'video', src:'https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4', user:'Ayesha', caption:'🔥🔥🔥', likes:'45K'},
  {type:'yt', id:'3JZ_D3ELwOQ', user:'YouTube', caption:'Music vibes 🎵', likes:'892K'},
];

let myVideos = []; // profile par upload ki hui videos

let chats = [
  {id:1, name:'Ali',   avatar:'🧑', msgs:[{me:false,t:'Kya haal hai?'},{me:true,t:'Bhai theek, tum sunao?'}]},
  {id:2, name:'Sara',  avatar:'👧', msgs:[{me:false,t:'Reels dekhi? 😂'}]},
  {id:3, name:'Bilal', avatar:'🧔', msgs:[{me:false,t:'Match dekhoge aaj? 🏏'}]},
];
const autoReplies = ['Haha 😂','Sahi hai!','Bilkul 👍','Acha ji','Wow 🤩','Phir baat karte hain'];
let activeChat = null;
let pendingVideo = null, svIndex = 0, svTimer = null, reelObserver = null;

const esc = s => s.replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

/* ================= NAVIGATION ================= */
function showScreen(name){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('open'));
  document.querySelectorAll('.bottom-nav button').forEach(b=>b.classList.remove('active'));
  if(name==='home'){ document.getElementById('nav-home').classList.add('active'); pauseAllReels(); window.scrollTo(0,0); return; }
  document.getElementById('nav-'+name).classList.add('active');
  document.getElementById('screen-'+name).classList.add('open');
  if(name==='reels') observeReels();
  if(name==='chat')  renderChats();
  if(name==='profile') renderProfile();
}
function closeScreen(name){
  document.getElementById('screen-'+name).classList.remove('open');
  document.getElementById('nav-'+name).classList.remove('active');
  pauseAllReels();
}

/* ================= STORIES ================= */
function renderStories(){
  document.getElementById('storiesBar').innerHTML = stories.map((s,i)=>`
    <div class="story ${s.seen?'seen':''}" onclick="openStory(${i})">
      <div class="ring"><div class="inner">${s.emoji}</div></div>
      <span>${s.name}</span>
    </div>`).join('');
}
function openStory(i){
  const s = stories[i];
  if(s.mine && !s.img){ document.getElementById('snapFile').click(); return; }
  svIndex = i;
  document.getElementById('storyViewer').classList.add('open');
  document.getElementById('svAvatar').textContent = s.emoji;
  document.getElementById('svName').textContent = s.name;
  const c = document.getElementById('svContent');
  c.style.background = s.bg || '#000';
  c.innerHTML = (s.img ? `<img src="${s.img}">` : `<div class="big">${s.emoji}</div><p style="font-size:20px;margin-top:10px">${s.text||''}</p>`)
    + `<div class="nav-l" onclick="prevStory()"></div><div class="nav-r" onclick="nextStory()"></div>`;
  const bar = document.getElementById('storyBar');
  bar.classList.remove('go'); void bar.offsetWidth; bar.classList.add('go');
  clearTimeout(svTimer);
  svTimer = setTimeout(nextStory, 5000);
  s.seen = true; renderStories();
}
function nextStory(){ svIndex < stories.length-1 ? openStory(svIndex+1) : closeStory(); }
function prevStory(){ if(svIndex>0) openStory(svIndex-1); }
function closeStory(){ clearTimeout(svTimer); document.getElementById('storyViewer').classList.remove('open'); }
function addMySnap(input){
  if(!input.files[0]) return;
  const s = stories.find(x=>x.mine);
  s.img = URL.createObjectURL(input.files[0]);
  s.emoji = '🙂'; s.bg = '#000'; s.seen = false;
  input.value = '';
  renderStories();
  openStory(stories.indexOf(s));
}

/* ================= FEED ================= */
function renderFeed(){
  document.getElementById('feed').innerHTML = feedPosts.map(p=>`
    <div class="post">
      <div class="post-head">
        <div class="avatar">${p.avatar}</div>
        <div><b>${p.user}</b><small>${p.time} pehle</small></div>
      </div>
      <video src="${p.video}" controls muted loop playsinline preload="metadata"></video>
      <div class="post-actions">
        <button onclick="this.textContent=this.textContent==='❤️'?'🤍':'❤️'">❤️</button>
        <button onclick="showScreen('chat')">💬</button>
        <button onclick="shareReel()">↗️</button>
      </div>
      <div class="post-caption"><b>${p.user}</b> ${p.caption}</div>
    </div>`).join('');
}

/* ================= REELS ================= */
function renderReels(){
  document.getElementById('reelsWrap').innerHTML = reels.map((r,i)=>{
    const media = r.type==='yt'
      ? `<iframe src="https://www.youtube.com/embed/${r.id}?enablejsapi=1&playsinline=1&mute=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" loading="lazy"></iframe>`
      : `<video src="${r.src}" loop muted playsinline></video>`;
    const badge = r.type==='yt' ? `<span class="yt-badge">▶ YouTube</span><br>` : '';
    return `<div class="reel">
      ${media}
      <div class="tap" onclick="tapReel(this,${i})"></div>
      <div class="reel-overlay">${badge}<b>@${esc(r.user)}</b><p>${esc(r.caption)}</p></div>
      <div class="reel-side">
        <div><button onclick="likeReel(this,${i})">❤️</button><small>${r.likes}</small></div>
        <div><button onclick="showScreen('chat')">💬</button><small>Comments</small></div>
        <div><button onclick="shareReel()">↗️</button><small>Share</small></div>
        <div><button onclick="toggleMute(this,${i})">🔇</button><small>Sound</small></div>
      </div>
    </div>`;
  }).join('');
}
function ytCommand(iframe, func){
  try{ iframe.contentWindow.postMessage(JSON.stringify({event:'command', func, args:[]}), '*'); }catch(e){}
}
function tapReel(btn, i){
  const reelEl = btn.closest('.reel');
  if(reels[i].type==='video'){
    const v = reelEl.querySelector('video');
    v.paused ? v.play() : v.pause();
  } else {
    const f = reelEl.querySelector('iframe');
    reelEl.dataset.paused = reelEl.dataset.paused==='1' ? '0' : '1';
    ytCommand(f, reelEl.dataset.paused==='1' ? 'pauseVideo' : 'playVideo');
  }
}
function toggleMute(btn, i){
  const reelEl = btn.closest('.reel');
  if(reels[i].type==='video'){
    const v = reelEl.querySelector('video');
    v.muted = !v.muted;
    btn.textContent = v.muted ? '🔇' : '🔊';
  } else {
    const f = reelEl.querySelector('iframe');
    const muteKaro = btn.textContent === '🔊';
    ytCommand(f, muteKaro ? 'mute' : 'unMute');
    btn.textContent = muteKaro ? '🔇' : '🔊';
  }
}
function likeReel(btn, i){
  btn.textContent = btn.textContent==='❤️' ? '🤍' : '❤️';
}
function observeReels(){
  if(reelObserver) reelObserver.disconnect();
  reelObserver = new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      const vid = e.target.querySelector('video');
      const yt  = e.target.querySelector('iframe');
      if(e.intersectionRatio > 0.6){
        if(vid) vid.play().catch(()=>{});
        if(yt)  ytCommand(yt,'playVideo');   // YouTube video khud chal jaye gi
      } else {
        if(vid) vid.pause();
        if(yt)  ytCommand(yt,'pauseVideo');
      }
    });
  }, {threshold:[0, 0.6, 1]});
  document.querySelectorAll('.reel').forEach(r=>reelObserver.observe(r));
}
function pauseAllReels(){
  document.querySelectorAll('#reelsWrap video').forEach(v=>v.pause());
  document.querySelectorAll('#reelsWrap iframe').forEach(f=>ytCommand(f,'pauseVideo'));
}
function shareReel(){
  const data = {title:'SnapReel', text:'Yeh video dekhein!', url: location.href};
  if(navigator.share) navigator.share(data).catch(()=>{});
  else { if(navigator.clipboard) navigator.clipboard.writeText(location.href); alert('Link copy ho gaya! 🔗'); }
}

/* ================= CHAT ================= */
function renderChats(){
  document.getElementById('chatList').style.display = 'block';
  document.getElementById('chatMsgs').style.display = 'none';
  document.getElementById('chatInputBar').style.display = 'none';
  document.getElementById('chatHead').innerHTML = '<span class="back" onclick="closeScreen(\'chat\')">←</span> Messages';
  document.getElementById('chatList').innerHTML = chats.map(c=>`
    <div class="chat-item" onclick="openChat(${c.id})">
      <div class="avatar">${c.avatar}</div>
      <div class="info"><b>${c.name}</b><small>${esc(c.msgs[c.msgs.length-1].t)}</small></div>
    </div>`).join('');
}
function openChat(id){
  activeChat = chats.find(c=>c.id===id);
  document.getElementById('chatHead').innerHTML =
    `<span class="back" onclick="renderChats()">←</span> <span style="font-size:20px">${activeChat.avatar}</span> ${activeChat.name}`;
  document.getElementById('chatList').style.display = 'none';
  document.getElementById('chatMsgs').style.display = 'flex';
  document.getElementById('chatInputBar').style.display = 'flex';
  renderMsgs();
}
function renderMsgs(){
  const box = document.getElementById('chatMsgs');
  box.innerHTML = activeChat.msgs.map(m=>`<div class="msg ${m.me?'me':'them'}">${esc(m.t)}</div>`).join('');
  box.scrollTop = box.scrollHeight;
}
function sendMsg(){
  const inp = document.getElementById('msgInput');
  const t = inp.value.trim();
  if(!t || !activeChat) return;
  activeChat.msgs.push({me:true, t});
  inp.value = '';
  renderMsgs();
  setTimeout(()=>{ // automatic reply
    if(!activeChat) return;
    activeChat.msgs.push({me:false, t: autoReplies[Math.floor(Math.random()*autoReplies.length)]});
    renderMsgs();
  }, 1200);
}

/* ================= PROFILE ================= */
function renderProfile(){
  document.getElementById('statPosts').textContent = myVideos.length;
  const grid = document.getElementById('videoGrid');
  grid.innerHTML = myVideos.length
    ? myVideos.map(v=>`<div class="tile" onclick="const v=this.querySelector('video'); v.paused?v.play():v.pause()"><video src="${v.src}" loop muted playsinline></video></div>`).join('')
    : `<div class="tile empty" onclick="openUpload()">➕</div><div class="tile empty">🎬</div><div class="tile empty">📹</div>`;
}

/* ================= UPLOAD ================= */
function openUpload(){ document.getElementById('uploadModal').classList.add('open'); }
function closeUpload(){
  document.getElementById('uploadModal').classList.remove('open');
  document.getElementById('preview').style.display = 'none';
  document.getElementById('videoCaption').value = '';
  document.getElementById('videoFile').value = '';
  pendingVideo = null;
}
function previewVideo(input){
  if(input.files[0]){
    pendingVideo = URL.createObjectURL(input.files[0]);
    const p = document.getElementById('preview');
    p.src = pendingVideo;
    p.style.display = 'block';
    p.play();
  }
}
function publish(where){
  if(!pendingVideo){ alert('Pehle video choose karein! 📁'); return; }
  const cap = document.getElementById('videoCaption').value.trim() || 'Meri video 🎬';
  if(where==='reel'){
    reels.unshift({type:'video', src:pendingVideo, user:'Aap', caption:cap, likes:'0'});
    renderReels();
    closeUpload();
    showScreen('reels');
  } else {
    myVideos.unshift({src:pendingVideo, caption:cap});
    renderProfile();
    closeUpload();
    showScreen('profile');
  }
}

/* ================= START ================= */
renderStories();
renderFeed();
renderReels();
renderProfile();
</script>
</body>
</html>
