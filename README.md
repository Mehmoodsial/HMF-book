# ============================================================
#  HMF BOOK — Instagram Demo App
#  File: app.py
# ============================================================
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Instagram", page_icon="📸", layout="wide")

st.markdown(
    "<style>#MainMenu{visibility:hidden}footer{visibility:hidden}"
    "header{visibility:hidden}</style>",
    unsafe_allow_html=True,
)

APP_HTML = r"""
<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Instagram</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Grand+Hotel&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--blue:#0095f6;--red:#ed4956;--line:#efefef;--line2:#dbdbdb;--t2:#737373}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{height:100%}
body{font-family:'Plus Jakarta Sans',sans-serif;background:#0d0d10;color:#0a0a0a;display:flex;align-items:center;justify-content:center;padding:26px}
button{background:none;border:0;font:inherit;color:inherit;cursor:pointer}
img{display:block;-webkit-user-drag:none;user-select:none}
input,textarea{font:inherit}
.iconw{display:inline-flex;align-items:center;justify-content:center}
.ic{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;flex:none}
.ic .fg{fill:currentColor;stroke:none}
.ic .cutk{stroke:#fff;stroke-width:2.3}
.vbadge{width:13px;height:13px}
.vbadge .fg{fill:#0095f6}
.phone{position:relative;width:min(400px,100%);height:min(860px,calc(100vh - 52px));background:#fff;border-radius:46px;overflow:hidden;border:1px solid #2a2a30;box-shadow:0 0 0 10px #17171b,0 40px 90px rgba(0,0,0,.6);display:flex;flex-direction:column}
.statusbar{height:36px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:8px 26px 0;background:#fff}
.sb-time{font-size:13.5px;font-weight:700}
.sb-ic{display:flex;gap:6px;align-items:center}
.app{position:relative;flex:1;overflow:hidden;background:#fff}
.screen{position:absolute;inset:0;overflow-y:auto;overscroll-behavior:contain;display:none;background:#fff;padding-bottom:calc(60px + env(safe-area-inset-bottom));scrollbar-width:none}
.screen::-webkit-scrollbar{display:none}
.screen.on{display:block;animation:scrIn .22s ease}
@keyframes scrIn{from{opacity:.4}to{opacity:1}}
.hd{position:sticky;top:0;z-index:6;display:flex;align-items:center;gap:12px;height:52px;padding:0 12px;background:rgba(255,255,255,.94);backdrop-filter:blur(10px);transition:transform .28s ease}
.hd.hid{transform:translateY(-110%)}
.hd .title{font-size:16.5px}
.logo{font-family:'Grand Hotel',cursive;font-size:28px;line-height:1;padding-top:4px}
.ml-auto{margin-left:auto}
.ib{display:flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;position:relative;flex:none;transition:transform .15s ease}
.ib:active{transform:scale(.85)}
.rel{position:relative}
.bdg{position:absolute;top:3px;right:1px;min-width:17px;height:17px;background:#ff3040;color:#fff;font-size:10.5px;font-weight:700;border-radius:9px;display:flex;align-items:center;justify-content:center;padding:0 4px;border:2px solid #fff}
.ring{display:block;padding:2.5px;border-radius:50%;background:conic-gradient(from 210deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5,#feda75)}
.ring.seen{background:var(--line2)}
.ring .in{display:block;padding:2.5px;background:#fff;border-radius:50%;width:100%;height:100%}
.ring img{width:100%;aspect-ratio:1;border-radius:50%;object-fit:cover}
.stories{display:flex;gap:6px;padding:10px 10px 12px;overflow-x:auto;border-bottom:1px solid var(--line);scrollbar-width:none}
.stories::-webkit-scrollbar{display:none}
.st-it{display:flex;flex-direction:column;align-items:center;gap:5px;width:72px;flex:none;position:relative}
.st-it .ring{width:66px;height:66px}
.st-nm{font-size:11.5px;color:#333;max-width:72px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.st-plus{position:absolute;top:40px;right:6px;width:20px;height:20px;border-radius:50%;background:var(--blue);color:#fff;border:2.5px solid #fff;display:flex;align-items:center;justify-content:center}
.st-plus .ic{width:11px;height:11px;stroke-width:3}
.post{padding-bottom:8px}
.post.new{animation:pIn .5s ease}
@keyframes pIn{from{opacity:0;transform:translateY(16px)}}
.p-hd{display:flex;align-items:center;gap:10px;padding:8px 12px}
.p-av{width:38px;height:38px;flex:none;display:flex;align-items:center;justify-content:center}
.p-av .ring{width:38px;height:38px}
.avw{display:flex;align-items:center;justify-content:center}
.avw img{width:34px;height:34px;border-radius:50%;object-fit:cover}
.p-handle{font-weight:700;font-size:13.5px;display:inline-flex;align-items:center;gap:3px}
.pd{color:var(--t2)}
.p-time{color:var(--t2);font-size:13px}
.flw{color:var(--blue);font-weight:700;font-size:13.5px;margin-left:6px}
.p-img{position:relative;aspect-ratio:4/5;background:#f4f4f4;overflow:hidden;cursor:pointer}
.p-img img{width:100%;height:100%;object-fit:cover}
.burst{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none;opacity:0}
.burst .ic{width:96px;height:96px;fill:#fff;stroke:none;filter:drop-shadow(0 6px 18px rgba(0,0,0,.35))}
.burst.go{animation:burst 1s ease forwards}
@keyframes burst{0%{opacity:0;transform:scale(.3)}18%{opacity:1;transform:scale(1.15)}32%{transform:scale(.95)}46%{transform:scale(1)}75%{opacity:1}100%{opacity:0;transform:scale(.9)}}
.p-act{display:flex;align-items:center;gap:5px;padding:4px 6px}
.likebtn.on .ic{fill:var(--red);stroke:var(--red)}
.likebtn.pop .ic{animation:pop .35s ease}
@keyframes pop{40%{transform:scale(1.3)}}
.savebtn.on .ic{fill:currentColor}
.p-likes{padding:0 12px;font-weight:700;font-size:13.5px}
.p-cap{padding:4px 12px 0;font-size:14px;line-height:1.45;cursor:pointer}
.p-cap b{margin-right:4px}
.p-cap.clamped{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.p-cm{display:block;padding:4px 12px 0;color:var(--t2);font-size:13.5px}
.srch{flex:1;display:flex;align-items:center;gap:8px;background:#efefef;border-radius:10px;padding:9px 12px}
.srch .ic{width:16px;height:16px;stroke-width:2;color:var(--t2)}
.srch input{flex:1;background:transparent;border:0;outline:0;font-size:14px;min-width:0}
.xbtn{color:var(--t2);display:flex}
.xbtn .ic{width:15px;height:15px;stroke-width:2.4}
.ex-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;grid-auto-flow:dense}
.tile{position:relative;aspect-ratio:1;overflow:hidden;background:#eee}
.tile.tall{grid-row:span 2;aspect-ratio:auto}
.tile img{width:100%;height:100%;object-fit:cover;transition:transform .35s ease}
.tile:active img{transform:scale(.94)}
.ex-empty{padding:70px 30px;text-align:center;color:var(--t2)}
.ex-empty b{display:block;font-size:17px;color:#000;margin-bottom:6px}
#scr-reels{padding-bottom:0;bottom:calc(52px + env(safe-area-inset-bottom));background:#000}
.rscroll{position:absolute;inset:0;overflow-y:auto;scroll-snap-type:y mandatory;scrollbar-width:none}
.rscroll::-webkit-scrollbar{display:none}
.reel{position:relative;height:100%;scroll-snap-align:start;scroll-snap-stop:always;overflow:hidden;background:#111}
.reel video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.r-scrim{position:absolute;left:0;right:0;bottom:0;height:38%;background:linear-gradient(to top,rgba(0,0,0,.62),transparent);pointer-events:none}
.r-info{position:absolute;left:12px;right:78px;bottom:18px;color:#fff;z-index:3}
.r-user{display:flex;align-items:center;gap:9px;font-size:13.5px}
.r-user img{width:32px;height:32px;border-radius:50%;object-fit:cover;border:1.5px solid #fff}
.r-flw{border:1.2px solid rgba(255,255,255,.85);color:#fff;font-size:12px;font-weight:700;border-radius:8px;padding:4px 10px;margin-left:2px}
.r-flw.fed{border-color:rgba(255,255,255,.4);color:rgba(255,255,255,.85)}
.r-cap{font-size:13px;margin:9px 0 7px;line-height:1.4;text-shadow:0 1px 8px rgba(0,0,0,.45)}
.r-music{display:flex;align-items:center;gap:7px;font-size:12.5px;overflow:hidden}
.r-music .ic{width:13px;height:13px}
.marq{overflow:hidden;flex:1;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent)}
.marq span{display:inline-block;white-space:nowrap;animation:mq 10s linear infinite}
@keyframes mq{to{transform:translateX(-50%)}}
.r-rail{position:absolute;right:6px;bottom:18px;display:flex;flex-direction:column;align-items:center;gap:15px;z-index:3;color:#fff}
.rr{display:flex;flex-direction:column;align-items:center;gap:3px;color:#fff;font-size:11.5px;font-weight:700}
.rr .ic{width:27px;height:27px;filter:drop-shadow(0 1px 6px rgba(0,0,0,.45))}
.rr.likebtn.on .ic{fill:var(--red);stroke:var(--red)}
.rr-disc{width:28px;height:28px;border-radius:50%;border:1.5px solid rgba(255,255,255,.7);overflow:hidden;animation:spin 7s linear infinite}
.rr-disc img{width:100%;height:100%;object-fit:cover}
@keyframes spin{to{transform:rotate(360deg)}}
.r-tap{position:absolute;inset:0 60px 0 0;z-index:2}
.r-flash{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;opacity:0;pointer-events:none;z-index:4}
.r-flash .ic{width:74px;height:74px;fill:rgba(255,255,255,.88);stroke:none}
.r-flash.go{animation:flash .5s ease}
@keyframes flash{15%{opacity:.9}100%{opacity:0;transform:scale(1.5)}}
.reels-top{position:absolute;top:8px;left:0;right:0;display:flex;align-items:center;justify-content:space-between;padding:2px 10px;z-index:6;color:#fff;pointer-events:none}
.reels-top b{font-size:17px;text-shadow:0 1px 10px rgba(0,0,0,.5)}
.mute{pointer-events:auto;width:36px;height:36px;border-radius:50%;background:rgba(15,15,15,.45);display:flex;align-items:center;justify-content:center;color:#fff}
.mute .ic{width:19px;height:19px}
.act-g{padding:12px 14px 4px;font-weight:700;font-size:14px}
.act-r{display:flex;align-items:center;gap:12px;padding:9px 14px}
.act-av{position:relative;width:44px;height:44px;flex:none}
.act-av img{width:100%;height:100%;border-radius:50%;object-fit:cover}
.act-av .mini{position:absolute;right:-4px;bottom:-4px;width:20px;height:20px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}
.mini .ic{width:12px;height:12px;stroke-width:2.6}
.mini.red .ic{fill:var(--red);stroke:var(--red)}
.mini.blue .ic{stroke:#0095f6}
.act-tx{flex:1;font-size:13.5px;line-height:1.45}
.act-tx .tm{color:var(--t2)}
.act-thumb{width:44px;height:44px;object-fit:cover;border-radius:4px}
.afb{background:var(--blue);color:#fff;font-weight:700;font-size:13px;border-radius:8px;padding:7px 14px;flex:none}
.afb.fed,.afb.ghost{background:#efefef;color:#000}
.req-btns{display:flex;gap:6px}
.dm-srch{padding:6px 14px 10px}
.dm-srch .srch{border-radius:12px}
.notes{display:flex;gap:20px;padding:14px;overflow-x:auto;border-bottom:1px solid var(--line);scrollbar-width:none}
.notes::-webkit-scrollbar{display:none}
.note{display:flex;flex-direction:column;align-items:center;gap:6px;width:76px;flex:none}
.note-b{position:relative;background:#efefef;border-radius:16px;padding:7px 11px;font-size:12px;font-weight:600;white-space:nowrap;max-width:110px;overflow:hidden;text-overflow:ellipsis}
.note-b:after{content:'';position:absolute;bottom:-6px;left:22px;border:6px solid transparent;border-top-color:#efefef;border-bottom:0}
.note img{width:56px;height:56px;border-radius:50%;object-fit:cover;border:2px solid var(--line2)}
.note .nm{font-size:11.5px}
.req-row{display:flex;align-items:center;gap:12px;width:100%;padding:10px 16px;border-bottom:1px solid var(--line);text-align:left}
.req-ic{width:44px;height:44px;border-radius:50%;background:#efefef;display:flex;align-items:center;justify-content:center;color:#000;flex:none}
.req-ic .ic{width:20px;height:20px;stroke-width:1.8}
.req-row b{font-size:14px}
.req-n{margin-left:auto;color:var(--t2);font-weight:700;font-size:13px}
.req-row .rrc{width:16px;height:16px;color:#c7c7c7;transform:rotate(-90deg);stroke-width:2.2}
.ch-row{display:flex;align-items:center;gap:12px;padding:9px 14px;cursor:pointer}
.ch-row:active{background:#fafafa}
.ch-av{position:relative;width:56px;height:56px;flex:none}
.ch-av img{width:100%;height:100%;border-radius:50%;object-fit:cover}
.on-dot{position:absolute;right:1px;bottom:1px;width:13px;height:13px;border-radius:50%;background:#2fd05a;border:2.5px solid #fff}
.ch-mid{flex:1;min-width:0}
.ch-mid>b{font-size:14px;display:flex;gap:3px;align-items:center}
.ch-prev{font-size:13px;color:var(--t2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}
.ch-prev.un{color:#000;font-weight:700}
.ch-cam{color:#000}
#scr-chat{display:none;flex-direction:column;padding-bottom:0;overflow:hidden}
#scr-chat.on{display:flex}
#scr-chat .hd{border-bottom:1px solid var(--line)}
.chat-id{display:flex;align-items:center;gap:10px;min-width:0}
.chat-id img{width:32px;height:32px;border-radius:50%;object-fit:cover}
.cname{font-size:14.5px;display:flex;align-items:center;gap:4px;font-weight:700}
.cstat{display:block;font-size:11.5px;color:var(--t2);font-weight:500}
.msgs{flex:1;overflow-y:auto;padding:0 12px 14px;display:flex;flex-direction:column;gap:5px;scrollbar-width:none}
.msgs::-webkit-scrollbar{display:none}
.intro{display:flex;flex-direction:column;align-items:center;text-align:center;padding:30px 20px 8px;gap:2px}
.intro-av img{width:84px;height:84px;border-radius:50%;object-fit:cover;margin-bottom:10px}
.intro b{font-size:15px;display:inline-flex;align-items:center;gap:4px}
.intro .iun{color:var(--t2);font-size:13px}
.intro .pbtn{margin-top:12px;width:auto;padding:7px 20px;flex:none}
.mrow{display:flex;max-width:80%}
.mrow.me{align-self:flex-end}
.mrow.them{align-self:flex-start}
.bub{padding:10px 14px;border-radius:22px;font-size:14.5px;line-height:1.4;word-break:break-word}
.them .bub{background:#efefef;border-bottom-left-radius:6px}
.me .bub{background:linear-gradient(135deg,#4F5BD5,#962FBF);color:#fff;border-bottom-right-radius:6px}
.imgb{padding:3px}
.imgb img{width:170px;border-radius:17px}
.hb{background:transparent!important;padding:2px}
.hb .ic{width:46px;height:46px;fill:var(--red);stroke:var(--red)}
.unsent{font-size:12.5px;color:var(--t2);font-style:italic;padding:4px 6px}
.day{align-self:center;font-size:11.5px;color:var(--t2);margin:6px 0 10px}
#typing .bub{display:flex;gap:4px;padding:13px 15px}
#typing i{width:7px;height:7px;border-radius:50%;background:#8e8e8e;animation:tp 1s infinite}
#typing i:nth-child(2){animation-delay:.15s}
#typing i:nth-child(3){animation-delay:.3s}
@keyframes tp{30%{transform:translateY(-4px);opacity:.5}}
.cbar{display:flex;align-items:center;gap:8px;padding:8px 10px calc(10px + env(safe-area-inset-bottom));border-top:1px solid var(--line);background:#fff}
.pill{flex:1;display:flex;align-items:center;gap:2px;border:1px solid var(--line2);border-radius:24px;padding:4px 6px 4px 8px;min-width:0}
.pill:focus-within{border-color:#bbb}
.pill .ib{width:30px;height:30px}
.pill .ib .ic{width:21px;height:21px;stroke-width:2}
#chat-inp{flex:1;border:0;padding:8px 6px 8px 2px;font-size:14px;outline:0;min-width:0}
.chat-r{display:flex;align-items:center;gap:2px}
.chat-r .ib .ic{width:22px;height:22px;stroke-width:1.8}
.snd{color:var(--blue);font-weight:700;font-size:14.5px;padding:6px}
.pf-top{display:flex;align-items:center;gap:26px;padding:8px 20px 4px}
.pf-av{width:88px;height:88px;flex:none}
.pf-av .ring{width:88px;height:88px}
.pf-stats{display:flex;flex:1;justify-content:space-around;text-align:center}
.pf-stats b{display:block;font-size:16.5px}
.pf-stats span{font-size:13px}
.pf-bio{padding:10px 20px 0;font-size:13.5px;line-height:1.5;white-space:pre-line}
.pf-bio b{display:block;margin-bottom:2px;white-space:normal}
.pf-link{margin:4px 20px 0;color:#00376b;font-weight:600;font-size:13.5px}
.pf-btns{display:flex;gap:8px;padding:14px 20px 10px}
.pbtn{flex:1;background:#efefef;border-radius:9px;padding:8px 0;font-weight:700;font-size:13.5px}
.pbtn:active{background:#e2e2e2}
.pf-hls{display:flex;gap:16px;padding:6px 20px 14px;overflow-x:auto;scrollbar-width:none}
.pf-hls::-webkit-scrollbar{display:none}
.hl{display:flex;flex-direction:column;align-items:center;gap:5px;font-size:11.5px;flex:none}
.hlc{width:62px;height:62px;border-radius:50%;border:1px solid var(--line2);padding:3px}
.hlc img{width:100%;height:100%;border-radius:50%;object-fit:cover}
.pf-tabs{display:flex;border-top:1px solid var(--line);margin-top:4px}
.pf-tabs button{flex:1;display:flex;justify-content:center;padding:11px 0;color:var(--line2);border-top:1.5px solid transparent;margin-top:-1px}
.pf-tabs button.on{color:#000;border-top-color:#000}
.pf-tabs .ic{width:22px;height:22px}
.pf-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;padding-bottom:20px}
.pf-t{position:relative;aspect-ratio:1;overflow:hidden;background:#f3f3f3}
.pf-t img{width:100%;height:100%;object-fit:cover}
.rvw .rv{position:absolute;left:6px;bottom:5px;color:#fff;font-size:11.5px;font-weight:700;display:flex;align-items:center;gap:4px;text-shadow:0 1px 4px rgba(0,0,0,.5)}
.rvw .rv .ic{width:13px;height:13px;fill:#fff;stroke:none}
.bnav{position:absolute;left:0;right:0;bottom:0;height:calc(52px + env(safe-area-inset-bottom));padding-bottom:env(safe-area-inset-bottom);display:flex;background:#fff;border-top:1px solid var(--line);z-index:40}
.bnav button{flex:1;display:flex;align-items:center;justify-content:center;transition:transform .12s}
.bnav button:active{transform:scale(.88)}
.bnav .ic{width:24px;height:24px}
.bnav button.on .ic{fill:currentColor;stroke-width:1.9}
.bnav button.on .cut{stroke:#fff}
.bnav button.on .cutf{fill:#fff}
.pavw{width:25px;height:25px;border-radius:50%;overflow:hidden;border:1.6px solid transparent;display:block}
.pavw.on{border-color:#000}
.pavw img{width:100%;height:100%;object-fit:cover}
.veil{position:absolute;inset:0;background:rgba(0,0,0,.5);opacity:0;pointer-events:none;transition:opacity .3s;z-index:84}
.veil.on{opacity:1;pointer-events:auto}
.sheet{position:absolute;left:0;right:0;bottom:0;z-index:85;background:#fff;border-radius:18px 18px 0 0;transform:translateY(105%);transition:transform .34s cubic-bezier(.32,.72,.24,1);max-height:78%;display:flex;flex-direction:column;padding-bottom:env(safe-area-inset-bottom)}
.sheet.up{transform:none}
.grab{width:36px;height:4px;background:#ddd;border-radius:2px;margin:8px auto 0;flex:none}
.sh-hd{position:relative;display:flex;align-items:center;padding:10px 12px;border-bottom:1px solid var(--line);flex:none;min-height:52px}
.sh-hd.ctr{justify-content:space-between;border-bottom:0;padding-top:4px}
.sh-hd.ctr b{position:absolute;left:50%;transform:translateX(-50%);font-size:15px}
.sh-blue{color:var(--blue);font-weight:700;font-size:14.5px;margin-left:auto}
.sh-blue:disabled{opacity:.35}
.sh-body{overflow-y:auto;scrollbar-width:none}
.sh-body::-webkit-scrollbar{display:none}
.cr-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}
.cr-t{position:relative;aspect-ratio:1;overflow:hidden}
.cr-t img{width:100%;height:100%;object-fit:cover}
.cr-t.sel:after{content:'';position:absolute;inset:0;border:3px solid #000}
.cr-up{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--t2);font-size:12px;font-weight:600;background:#fafafa}
.cr-up .ic{width:26px;height:26px}
.cr-prev img{width:100%;max-height:44vh;object-fit:contain;background:#000}
#cr-cap{width:100%;border:0;outline:0;padding:14px 16px;font-size:14px;resize:none}
.cm-list{overflow-y:auto;padding:6px 0;min-height:120px;scrollbar-width:none}
.cm-list::-webkit-scrollbar{display:none}
.cm-r{display:flex;gap:11px;padding:8px 16px;font-size:13.5px;line-height:1.45}
.cm-r img{width:32px;height:32px;border-radius:50%;object-fit:cover;flex:none}
.cm-r b{margin-right:5px}
.cm-r .ct{color:var(--t2);font-size:12px;margin-top:3px}
.cm-foot{display:flex;align-items:center;gap:9px;border-top:1px solid var(--line);padding:9px 14px}
.cm-foot img{width:30px;height:30px;border-radius:50%}
#cm-inp{flex:1;border:0;outline:0;font-size:14px;min-width:0}
#cm-post{color:var(--blue);font-weight:700;font-size:14px}
.shr-list{overflow-y:auto;padding:4px 0 10px;scrollbar-width:none}
.shr-list::-webkit-scrollbar{display:none}
.shr-r{display:flex;align-items:center;gap:12px;padding:8px 16px;cursor:pointer}
.shr-r img{width:44px;height:44px;border-radius:50%;object-fit:cover}
.shr-avw{position:relative;width:44px;height:44px;flex:none}
.shr-n{flex:1;font-size:14px;font-weight:600;min-width:0}
.shr-n small{display:block;color:var(--t2);font-weight:500;font-size:12px}
.shr-send{color:var(--blue);font-weight:700;font-size:13.5px;padding:8px}
.shr-chev{color:#bbb;display:flex}
.menu-list{padding:6px 0 10px}
.mn{display:block;width:100%;padding:14px 18px;font-size:14.5px;font-weight:600;text-align:center;border-top:1px solid var(--line)}
.mn:first-child{border-top:0}
.mn.danger{color:var(--red);font-weight:700}
.ed-body{padding:16px;display:flex;flex-direction:column;gap:14px}
.ed-body label{font-size:12.5px;font-weight:700;color:var(--t2);display:flex;flex-direction:column;gap:6px}
.ed-body input,.ed-body textarea{border:1px solid var(--line2);border-radius:10px;padding:10px 12px;font-size:14px;outline:0;resize:none}
.pv{position:absolute;inset:0;background:#050505;z-index:70;display:none;flex-direction:column}
.pv.on{display:flex}
.pv-hd{display:flex;justify-content:flex-end;padding:6px;color:#fff}
.pv-imgw{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}
.pv-imgw img{max-width:100%;max-height:100%;object-fit:contain}
.pv-meta{display:flex;align-items:center;gap:10px;padding:8px 14px;color:#fff}
.pv-meta>img{width:32px;height:32px;border-radius:50%;object-fit:cover}
.pv-user{flex:1;font-size:13.5px;font-weight:700;display:flex;gap:5px;align-items:center}
.pv-acts{display:flex;gap:2px}
.pv-likes{padding:0 16px 22px;font-weight:700;font-size:13.5px}
.sv{position:absolute;inset:0;background:#000;z-index:80;display:none}
.sv.on{display:block}
.sv-imgw{position:absolute;inset:0;overflow:hidden}
.sv-imgw img{width:100%;height:100%;object-fit:cover}
.sv-imgw img.kb{animation:kb 6.5s linear forwards}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.1) translate(-1.5%,1%)}}
.sv-segs{position:absolute;top:8px;left:10px;right:10px;display:flex;gap:4px;z-index:6}
.sv-segs i{flex:1;height:2.5px;background:rgba(255,255,255,.35);border-radius:2px;overflow:hidden}
.sv-segs b{display:block;height:100%;width:0;background:#fff}
.sv-hd{position:absolute;top:20px;left:0;right:0;display:flex;align-items:center;gap:10px;padding:8px 12px;color:#fff;z-index:6}
.sv-hd .sv-av img{width:34px;height:34px;border-radius:50%;object-fit:cover;border:1.5px solid rgba(255,255,255,.9)}
.sv-hd b{font-size:13.5px}
.sv-t{color:rgba(255,255,255,.75);font-size:12.5px}
.sv-zone{position:absolute;top:70px;bottom:70px;z-index:5}
.sv-zone.l{left:0;width:32%}
.sv-zone.r{right:0;width:68%}
.sv-ft{position:absolute;left:0;right:0;bottom:0;display:flex;align-items:center;gap:8px;padding:10px 12px calc(14px + env(safe-area-inset-bottom));z-index:6}
#sv-inp{flex:1;border:1.2px solid rgba(255,255,255,.75);background:transparent;border-radius:22px;padding:9px 15px;color:#fff;font-size:13.5px;outline:0;min-width:0}
#sv-inp::placeholder{color:rgba(255,255,255,.8)}
.sv-ft .ib{color:#fff}
.toast{position:absolute;left:50%;bottom:80px;transform:translate(-50%,16px);background:#262626;color:#fff;padding:10px 18px;border-radius:24px;font-size:13.5px;font-weight:600;opacity:0;transition:.28s;z-index:99;pointer-events:none;white-space:nowrap;max-width:92%;overflow:hidden;text-overflow:ellipsis}
.toast.on{opacity:1;transform:translate(-50%,0)}
</style>
</head>
<body>
<div class="phone">
 <div class="statusbar">
  <span class="sb-time">9:41</span>
  <span class="sb-ic">
   <svg width="18" height="12"><rect y="7" width="3" height="5" rx="1" fill="#000"/><rect x="5" y="5" width="3" height="7" rx="1" fill="#000"/><rect x="10" y="2.5" width="3" height="9.5" rx="1" fill="#000"/><rect x="15" width="3" height="12" rx="1" fill="#000"/></svg>
   <svg width="17" height="12" viewBox="0 0 17 12"><path d="M2 5a9.2 9.2 0 0 1 13 0" stroke="#000" fill="none" stroke-width="1.7" stroke-linecap="round"/><path d="M4.6 7.7a5.5 5.5 0 0 1 7.8 0" stroke="#000" fill="none" stroke-width="1.7" stroke-linecap="round"/><circle cx="8.5" cy="10.3" r="1.5" fill="#000"/></svg>
   <svg width="25" height="12" viewBox="0 0 25 12"><rect x=".5" y=".5" width="21" height="11" rx="3" fill="none" stroke="#000" opacity=".4"/><rect x="2" y="2" width="15" height="8" rx="1.8" fill="#000"/><path d="M23 4v4c1-.2 1.7-1 1.7-2S24 4.2 23 4z" fill="#000" opacity=".4"/></svg>
  </span>
 </div>
 <div class="app" id="app">
  <section class="screen on" id="scr-feed">
   <header class="hd" id="feed-hd">
    <span class="logo">Instagram</span>
    <span class="ml-auto"></span>
    <button class="ib rel" id="hb-act"><span class="iconw" data-icon="heart"></span><span class="bdg" id="bdg-act">3</span></button>
    <button class="ib rel" id="hb-dm"><span class="iconw" data-icon="plane"></span><span class="bdg" id="bdg-dm">3</span></button>
   </header>
   <div class="stories" id="stories"></div>
   <div id="feed"></div>
  </section>
  <section class="screen" id="scr-explore">
   <header class="hd">
    <div class="srch">
     <span class="iconw" data-icon="search"></span>
     <input id="ex-q" placeholder="Search" autocomplete="off">
     <button class="xbtn" id="ex-clear" hidden><span class="iconw" data-icon="x"></span></button>
    </div>
   </header>
   <div class="ex-grid" id="ex-grid"></div>
   <div class="ex-empty" id="ex-empty" hidden><b>Kuch nahi mila</b>Dusre keywords se try karo</div>
  </section>
  <section class="screen" id="scr-reels">
   <div class="rscroll" id="rscroll"></div>
   <div class="reels-top"><b>Reels</b><button class="mute" id="reels-mute"></button></div>
  </section>
  <section class="screen" id="scr-activity">
   <header class="hd"><button class="ib" data-back="feed"><span class="iconw" data-icon="back"></span></button><b class="title">Notifications</b></header>
   <div id="act-list"></div>
  </section>
  <section class="screen" id="scr-messages">
   <header class="hd">
    <button class="ib" data-back="feed"><span class="iconw" data-icon="back"></span></button>
    <b class="title">aarav_wanders</b>
    <span class="iconw" data-icon="chev" style="color:#888"></span>
    <span class="ml-auto"></span>
    <button class="ib" id="dm-new"><span class="iconw" data-icon="compose"></span></button>
   </header>
   <div class="dm-srch">
    <div class="srch">
     <span class="iconw" data-icon="search"></span>
     <input id="dm-q" placeholder="Ask Meta AI or search" autocomplete="off">
    </div>
   </div>
   <div class="notes" id="notes"></div>
   <button class="req-row" id="req-row">
    <span class="req-ic"><span class="iconw" data-icon="heart"></span></span>
    <b>Requests</b>
    <span class="req-n" id="req-n">2</span>
    <span class="iconw rrc" data-icon="chev"></span>
   </button>
   <div id="chat-list"></div>
  </section>
  <section class="screen" id="scr-chat">
   <header class="hd">
    <button class="ib" data-back="messages"><span class="iconw" data-icon="back"></span></button>
    <div class="chat-id"><span class="rel"><img id="ch-av" alt=""><i class="on-dot" id="ch-dot" hidden></i></span><div><span class="cname" id="ch-name"></span><span class="cstat" id="ch-stat"></span></div></div>
    <span class="ml-auto"></span>
    <button class="ib" data-call="phone"><span class="iconw" data-icon="phone"></span></button>
    <button class="ib" data-call="video"><span class="iconw" data-icon="video"></span></button>
   </header>
   <div class="msgs" id="msgs"></div>
   <footer class="cbar">
    <div class="pill">
     <button class="ib" id="chat-cam"><span class="iconw" data-icon="camera"></span></button>
     <input id="chat-inp" placeholder="Message…" autocomplete="off">
    </div>
    <span class="chat-r" id="chat-r">
     <button class="ib" id="chat-mic"><span class="iconw" data-icon="mic"></span></button>
     <button class="ib" id="chat-img"><span class="iconw" data-icon="img"></span></button>
     <button class="ib" id="chat-smile"><span class="iconw" data-icon="smile"></span></button>
     <button class="ib" id="chat-heart"><span class="iconw" data-icon="heart"></span></button>
    </span>
    <button class="snd" id="chat-send" hidden>Send</button>
   </footer>
   <input type="file" id="chat-file" accept="image/*" hidden>
  </section>
  <section class="screen" id="scr-profile">
   <header class="hd">
    <b class="title">aarav_wanders</b>
    <span class="ml-auto"></span>
    <button class="ib" id="pf-add"><span class="iconw" data-icon="plusS"></span></button>
    <button class="ib" id="pf-menu"><span class="iconw" data-icon="menu"></span></button>
   </header>
   <div class="pf-top">
    <span class="pf-av" id="pf-av"></span>
    <div class="pf-stats">
     <div><b id="st-posts">0</b><span>posts</span></div>
     <div><b id="st-followers">0</b><span>followers</span></div>
     <div><b id="st-following">0</b><span>following</span></div>
    </div>
   </div>
   <div class="pf-bio"><b id="pf-name">Aarav</b><span id="pf-bio">Delhi NCR · Chai over coffee
Travel · Street · Films</span></div>
   <button class="pf-link" id="pf-link">bit.ly/aarav-films</button>
   <div class="pf-btns"><button class="pbtn" id="pf-edit">Edit profile</button><button class="pbtn" id="pf-share">Share profile</button></div>
   <div class="pf-hls" id="pf-hls"></div>
   <div class="pf-tabs">
    <button class="on" data-tab="posts"><span class="iconw" data-icon="grid"></span></button>
    <button data-tab="reels"><span class="iconw" data-icon="reels"></span></button>
    <button data-tab="tagged"><span class="iconw" data-icon="tag"></span></button>
   </div>
   <div class="pf-grid" id="pf-grid"></div>
  </section>
  <section class="screen" id="scr-saved">
   <header class="hd"><button class="ib" data-back="profile"><span class="iconw" data-icon="back"></span></button><b class="title">Saved</b></header>
   <div class="ex-grid" id="sv-grid"></div>
   <div class="ex-empty" id="sv-empty" hidden><b>Kuch saved nahi hai</b>Post mein bookmark icon dabao, yahan dikhega</div>
  </section>
  <nav class="bnav" id="bnav">
   <button data-go="feed" class="on"><span class="iconw" data-icon="home"></span></button>
   <button data-go="explore"><span class="iconw" data-icon="search"></span></button>
   <button data-go="create" id="nav-create"><span class="iconw" data-icon="plus"></span></button>
   <button data-go="reels"><span class="iconw" data-icon="reels"></span></button>
   <button data-go="profile"><span class="pavw" id="nav-pav"><img alt=""></span></button>
  </nav>
  <div class="pv" id="pv">
   <div class="pv-hd"><button class="ib" id="pv-x"><span class="iconw" data-icon="x"></span></button></div>
   <div class="pv-imgw"><img id="pv-img" alt=""></div>
   <div class="pv-meta">
    <img id="pv-av" alt=""><span class="pv-user" id="pv-user"></span>
    <div class="pv-acts">
     <button class="ib likebtn" id="pv-like"></button>
     <button class="ib" id="pv-cm"></button>
     <button class="ib" id="pv-share"></button>
    </div>
   </div>
   <div class="pv-likes" id="pv-likes"></div>
  </div>
  <div class="sv" id="sv">
   <div class="sv-imgw"><img id="sv-img" alt=""></div>
   <div class="sv-segs" id="sv-segs"></div>
   <header class="sv-hd"><span class="sv-av" id="sv-av"></span><b id="sv-name"></b><span class="sv-t" id="sv-time"></span><button class="ib sv-x" id="sv-x"><span class="iconw" data-icon="x"></span></button></header>
   <div class="sv-zone l" id="sv-prev"></div>
   <div class="sv-zone r" id="sv-next"></div>
   <footer class="sv-ft">
    <input id="sv-inp" placeholder="Reply to story…" autocomplete="off">
    <button class="ib" id="sv-like"><span class="iconw" data-icon="heart"></span></button>
    <button class="ib" id="sv-share"><span class="iconw" data-icon="plane"></span></button>
   </footer>
  </div>
  <div class="veil" id="veil"></div>
  <div class="sheet" id="sh-share">
   <div class="grab"></div>
   <header class="sh-hd ctr"><span></span><b id="shr-title">Share</b><button class="ib" id="shr-x"><span class="iconw" data-icon="x"></span></button></header>
   <div class="shr-list" id="shr-list"></div>
  </div>
  <div class="sheet" id="sh-cm">
   <div class="grab"></div>
   <header class="sh-hd ctr"><span></span><b>Comments</b><button class="ib" id="cm-x"><span class="iconw" data-icon="x"></span></button></header>
   <div class="cm-list" id="cm-list"></div>
   <footer class="cm-foot"><img id="cm-av" alt=""><input id="cm-inp" placeholder="Comment add karo…" autocomplete="off"><button id="cm-post">Post</button></footer>
  </div>
  <div class="sheet" id="sh-create">
   <header class="sh-hd"><button class="ib" id="cr-x"><span class="iconw" data-icon="x"></span></button><b id="cr-title">New post</b><button class="sh-blue" id="cr-next" disabled>Next</button></header>
   <div class="sh-body" id="cr-step1"><div class="cr-grid" id="cr-grid"></div></div>
   <div class="sh-body" id="cr-step2" hidden><div class="cr-prev"><img id="cr-img" alt=""></div><textarea id="cr-cap" rows="3" placeholder="Caption likho…"></textarea></div>
  </div>
  <div class="sheet" id="sh-menu"><div class="grab"></div><div class="menu-list" id="menu-list"></div></div>
  <div class="sheet" id="sh-edit">
   <header class="sh-hd"><button class="ib" id="ed-x"><span class="iconw" data-icon="x"></span></button><b>Edit profile</b><button class="sh-blue" id="ed-save">Save</button></header>
   <div class="ed-body">
    <label>Name<input id="ed-name"></label>
    <label>Bio<textarea id="ed-bio" rows="3"></textarea></label>
   </div>
  </div>
  <div class="toast" id="toast"></div>
 </div>
</div>
<script>
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const ph=(seed,w=900,h=1125)=>`https://picsum.photos/seed/${seed}/${w}/${h}`;
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const fmt=n=>n.toLocaleString('en-IN');
const kfmt=n=>n>=1e6?(n/1e6).toFixed(1).replace('.0','')+'M':n>=1e3?(n/1e3).toFixed(1).replace('.0','')+'K':n;
const nowT=()=>new Date().toTimeString().slice(0,5);
const ICONS={
home:'<path d="M9.3 20.5v-5.3a1.2 1.2 0 0 1 1.2-1.2h3a1.2 1.2 0 0 1 1.2 1.2v5.3h3.9a1.4 1.4 0 0 0 1.4-1.4v-8.5c0-.43-.2-.83-.53-1.1l-7.35-6.02a1.4 1.4 0 0 0-1.77 0L3.13 9.5c-.33.27-.53.67-.53 1.1v8.5a1.4 1.4 0 0 0 1.4 1.4z"/>',
search:'<circle cx="10.7" cy="10.7" r="7.2"/><path d="m16 16 5.2 5.2"/>',
plus:'<rect x="3" y="3" width="18" height="18" rx="4.6"/><path class="cut" d="M12 7.8v8.4M7.8 12h8.4"/>',
reels:'<rect x="2.8" y="2.8" width="18.4" height="18.4" rx="4.8"/><path d="M2.8 8.7h18.4M8.6 2.9 5.7 8.7M15.5 2.9l-2.9 5.8"/><path class="cut cutf" d="m10.7 11.9 4.9 2.8-4.9 2.8z"/>',
user:'<circle cx="12" cy="7.9" r="4.1"/><path d="M4.6 20.4c.9-3.4 3.9-5.4 7.4-5.4s6.5 2 7.4 5.4"/>',
heart:'<path d="M12 20.8S3.4 15.5 3.4 9.8c0-2.9 2.3-5.2 5.1-5.2 1.6 0 3 .9 3.5 2 .5-1.1 1.9-2 3.5-2 2.8 0 5.1 2.3 5.1 5.2 0 5.7-8.6 11-8.6 11z"/>',
comment:'<path d="M12 3.1c-5 0-9.1 3.6-9.1 8.1 0 2.5 1.3 4.8 3.3 6.3v3.4l3.3-1.9c.8.2 1.6.3 2.5.3 5 0 9.1-3.6 9.1-8.1S17 3.1 12 3.1z"/>',
plane:'<path d="M21.5 2.5a1 1 0 0 0-1.05-.22L2.8 8.7a1 1 0 0 0 .07 1.9l6.9 2.13a1 1 0 0 1 .65.65l2.14 6.9a1 1 0 0 0 1.9.07l6.4-17.65a1 1 0 0 0-.36-1.1z"/><path d="M21.3 2.7 10.3 13.7"/>',
bookmark:'<path d="M6.5 3.5h11a1.3 1.3 0 0 1 1.3 1.3v15.9l-6.8-4.5-6.8 4.5V4.8a1.3 1.3 0 0 1 1.3-1.3z"/>',
ellipsis:'<circle class="fg" cx="4.7" cy="12" r="1.55"/><circle class="fg" cx="12" cy="12" r="1.55"/><circle class="fg" cx="19.3" cy="12" r="1.55"/>',
back:'<path d="M15 4.6 7.6 12l7.4 7.4"/>',
chev:'<path d="m6.5 9.3 5.5 5.4 5.5-5.4"/>',
camera:'<path d="M4 8.4c0-1.1.9-2 2-2h1.5l1.2-1.8c.28-.42.75-.6 1.2-.6h4.2c.45 0 .92.18 1.2.6l1.3 1.8H18a2 2 0 0 1 2 2v8.4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/><circle cx="12" cy="12.4" r="3.5"/>',
x:'<path d="M5.8 5.8 18.2 18.2M18.2 5.8 5.8 18.2"/>',
volx:'<path class="fg" d="M11.4 4.9 6.9 8.6H4.1a1 1 0 0 0-1 1v4.8a1 1 0 0 0 1 1h2.8l4.5 3.7c.66.54 1.6.07 1.6-.78V5.68c0-.85-.94-1.32-1.6-.78z"/><path d="m15.8 9.7 4.6 4.6M20.4 9.7l-4.6 4.6"/>',
vol:'<path class="fg" d="M11.4 4.9 6.9 8.6H4.1a1 1 0 0 0-1 1v4.8a1 1 0 0 0 1 1h2.8l4.5 3.7c.66.54 1.6.07 1.6-.78V5.68c0-.85-.94-1.32-1.6-.78z"/><path d="M16 9a4.3 4.3 0 0 1 0 6M18.6 6.6a8 8 0 0 1 0 10.8"/>',
play:'<path class="fg" d="M8.2 5.9c0-.83.9-1.34 1.6-.92l8.5 5.1c.68.4.68 1.4 0 1.8l-8.5 5.1c-.7.42-1.6-.09-1.6-.92z"/>',
grid:'<path class="fg" d="M3.8 3.8h4.9v4.9H3.8zM9.55 3.8h4.9v4.9h-4.9zM15.3 3.8h4.9v4.9h-4.9zM3.8 9.55h4.9v4.9H3.8zM9.55 9.55h4.9v4.9h-4.9zM15.3 9.55h4.9v4.9h-4.9zM3.8 15.3h4.9v4.9H3.8zM9.55 15.3h4.9v4.9h-4.9zM15.3 15.3h4.9v4.9h-4.9z"/>',
tag:'<circle cx="10.6" cy="8.4" r="3.4"/><path d="M4.1 19.7c.8-3.3 3.4-5.1 6.5-5.1 1 0 2 .2 2.8.6"/><path d="m17.6 12.9 3 3-4.6 4.6-2.9.6.6-2.9z"/>',
menu:'<path d="M4 7h16M4 12h16M4 17h16"/>',
compose:'<path d="M20 12.6v5.2a2.2 2.2 0 0 1-2.2 2.2H6.2A2.2 2.2 0 0 1 4 17.8V6.2A2.2 2.2 0 0 1 6.2 4h5.2"/><path d="M18.7 3.5a1.9 1.9 0 0 1 2.7 2.7l-8 8-3.6.9.9-3.6z"/>',
verified:'<circle class="fg" cx="12" cy="12" r="10"/><path class="cutk" d="m7.7 12.4 2.9 2.9 5.7-6.1"/>',
music:'<path class="fg" d="M9.6 18.1a2.6 2.6 0 1 1-1.7-2.45V6.4c0-.47.33-.88.8-.98l7.5-1.55a1 1 0 0 1 1.2.98v10.75a2.6 2.6 0 1 1-1.7-2.45V7.5l-6.1 1.26z"/>',
plusS:'<path d="M12 5.3v13.4M5.3 12h13.4"/>',
phone:'<path d="M6.8 3.6 8.9 3a1.1 1.1 0 0 1 1.3.7l1 2.9a1.1 1.1 0 0 1-.3 1.2L9.6 8.9a12.7 12.7 0 0 0 5.5 5.5l1.1-1.3a1.1 1.1 0 0 1 1.2-.3l2.9 1a1.1 1.1 0 0 1 .7 1.3l-.6 2.1a2 2 0 0 1-2 1.5C10.7 18.4 5.6 13.3 5.3 5.6a2 2 0 0 1 1.5-2z"/>',
video:'<rect x="2.8" y="6" width="13" height="12" rx="3.4"/><path d="m15.8 12.6 4.2 2.7c.7.44 1.6-.06 1.6-.88V7.6c0-.82-.9-1.32-1.6-.88l-4.2 2.7"/>',
mic:'<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
img:'<rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8.8" cy="8.8" r="1.7"/><path d="m4 17 4.8-4.8a1.4 1.4 0 0 1 2 0l6.4 6.4M14 14l1.8-1.8a1.4 1.4 0 0 1 2 0l3 3"/>',
smile:'<circle cx="12" cy="12" r="8.6"/><path d="M8.7 14a4.2 4.2 0 0 0 6.6 0"/><circle class="fg" cx="9.2" cy="10" r="1.1"/><circle class="fg" cx="14.8" cy="10" r="1.1"/>'
};
const ic=(n,c='')=>`<svg class="ic ${c}" viewBox="0 0 24 24" aria-hidden="true">${ICONS[n]}</svg>`;
 $$('[data-icon]').forEach(el=>el.innerHTML=ic(el.dataset.icon));
const U={
 you:{h:'aarav_wanders',n:'Aarav',av:'https://i.pravatar.cc/150?img=12'},
 kabir:{h:'mehra_films',n:'Kabir Mehra',v:1,av:'https://i.pravatar.cc/150?img=53',lastSeen:'1h ago'},
 sneha:{h:'sneha.klicks',n:'Sneha Kapoor',av:'https://i.pravatar.cc/150?img=44',online:1},
 rohan:{h:'rohan_trails',n:'Rohan Iyer',av:'https://i.pravatar.cc/150?img=68',lastSeen:'2h ago'},
 ananya:{h:'ananya.ink',n:'Ananya Rao',v:1,av:'https://i.pravatar.cc/150?img=25',lastSeen:'1d ago'},
 dfr:{h:'delhifoodroute',n:'Delhi Food Route',av:'https://i.pravatar.cc/150?img=20',lastSeen:'3h ago',followed:1},
 tanya:{h:'tanya.moves',n:'Tanya Sharma',av:'https://i.pravatar.cc/150?img=47',online:1},
 vihaan:{h:'imvihaan',n:'Vihaan',av:'https://i.pravatar.cc/150?img=15',lastSeen:'23m ago'},
 leaf:{h:'leafandlens',n:'Leaf & Lens',av:'https://i.pravatar.cc/150?img=60',lastSeen:'2d ago',followed:1},
};
const avImg=(u,st='')=>`<img ${st} src="${U[u].av}" alt="${esc(U[u].n)}" onerror="this.onerror=null;this.src='https://picsum.photos/seed/av-${u}/150'">`;
const posts=[
 {id:'p1',u:'sneha',img:ph('ig-sunrise'),likes:1284,t:'3h',cap:'4 baje ki alarm ki keemat… Golden hour hi asli hai.',cm:[{u:'rohan',t:'Worth it. Kya frame hai',tm:'2h'},{u:'ananya',t:'Colours bilkul unreal lag rahe hain',tm:'2h'},{u:'tanya',t:'Location batao na please!',tm:'1h'}]},
 {id:'p2',u:'dfr',img:ph('ig-butter'),likes:3402,t:'5h',cap:'Chandni Chowk ka asli butter chicken. Line lagane ke bhi din aa gaye.',cm:[{u:'kabir',t:'Ab raat ko bhookh nahi lagegi, thanks',tm:'4h'},{u:'vihaan',t:'Kal wahan ja rahe hain, table book karwado',tm:'3h'},{u:'sneha',t:'50mm pe shoot kiya na?',tm:'2h'}]},
 {id:'p3',u:'ananya',img:ph('ig-mural'),likes:892,t:'8h',cap:'Naya wall, purani galli. 3 din ka kaam, 6 spray cans.',cm:[{u:'leaf',t:'Wall ne toh gallery ban gayi',tm:'6h'},{u:'dfr',t:'Next mural cafe ke bahar karo',tm:'5h'}]},
 {id:'p4',u:'kabir',img:ph('ig-bts'),likes:2133,t:'12h',cap:'BTS from yesterday. Monitor dekhte hi pata chal gaya tha shot set hai.',cm:[{u:'rohan',t:'BTS hamesha best hota hai',tm:'9h'},{u:'tanya',t:'Light setup dekh ke maza aa gaya',tm:'8h'}]},
 {id:'p5',u:'rohan',img:ph('ig-trail'),likes:647,t:'1d',cap:'Triund done. 9 km, zero regrets. Next stop — Bijli Mahadev.',cm:[{u:'kabir',t:'Wapas kab?',tm:'20h'},{u:'vihaan',t:'Agli baar main bhi chalunga pakka',tm:'18h'}]},
];
const stories=[
 {u:'you',items:[],seen:1},
 {u:'sneha',items:[{img:ph('st-sneha1',720,1280),t:'2h'},{img:ph('st-sneha2',720,1280),t:'1h'}]},
 {u:'kabir',items:[{img:ph('st-kabir1',720,1280),t:'3h'},{img:ph('st-kabir2',720,1280),t:'2h'},{img:ph('st-kabir3',720,1280),t:'1h'}]},
 {u:'tanya',items:[{img:ph('st-tanya1',720,1280),t:'4h'},{img:ph('st-tanya2',720,1280),t:'3h'}]},
 {u:'rohan',items:[{img:ph('st-rohan1',720,1280),t:'5h'},{img:ph('st-rohan2',720,1280),t:'4h'}]},
 {u:'ananya',items:[{img:ph('st-ananya1',720,1280),t:'7h'}]},
];
const V='https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/';
const reels=[
 {id:'r1',u:'tanya',vid:V+'ForBiggerBlazes.mp4',poster:ph('rl-tanya',720,1280),cap:'200th take tha, but finally perfect.',music:'Tanya Sharma · Original audio',likes:12500,liked:0,cmN:214,cm:[{u:'kabir',t:'Killer moves',tm:'1h'},{u:'sneha',t:'Song kaun sa hai?',tm:'1h'}]},
 {id:'r2',u:'kabir',vid:V+'ForBiggerEscapes.mp4',poster:ph('rl-kabir',720,1280),cap:'Golden hour b-roll. Colour grade bhi khud kiya.',music:'cinematic loops · kabir',likes:8400,liked:0,cmN:98,cm:[{u:'rohan',t:'Grade next time mujhe sikha de',tm:'2h'}]},
 {id:'r3',u:'dfr',vid:V+'ForBiggerFun.mp4',poster:ph('rl-dfr',720,1280),cap:'POV: first bite of the day.',music:'trending · food sounds',likes:25300,liked:0,cmN:512,cm:[{u:'vihaan',t:'Bhai muh mein pani aa gaya',tm:'40m'},{u:'tanya',t:'Diet kal se, aaj nahi',tm:'30m'}]},
 {id:'r4',u:'vihaan',vid:V+'ForBiggerJoyrides.mp4',poster:ph('rl-vihaan',720,1280),cap:'Sunday ride. Sirf vibes.',music:'Original audio · vihaan',likes:4100,liked:0,cmN:67,cm:[{u:'rohan',t:'Next ride mein main bhi',tm:'3h'}]},
];
const explore=[
 {seed:'ex-street',tags:['city','street'],u:'vihaan',likes:842,cm:[],liked:0},
 {seed:'ex-cafe',tags:['food','cafe'],u:'dfr',likes:1930,cm:[],liked:0},
 {seed:'ex-peak',tags:['travel','nature','mountain'],u:'rohan',likes:3204,cm:[],liked:0,tall:1},
 {seed:'ex-neon',tags:['city','night'],u:'kabir',likes:2140,cm:[],liked:0,tall:1},
 {seed:'ex-mural',tags:['art'],u:'ananya',likes:964,cm:[],liked:0},
 {seed:'ex-thali',tags:['food'],u:'dfr',likes:1530,cm:[],liked:0},
 {seed:'ex-dune',tags:['travel','desert'],u:'rohan',likes:1102,cm:[],liked:0},
 {seed:'ex-monsoon',tags:['nature','rain'],u:'leaf',likes:1877,cm:[],liked:0,tall:1},
 {seed:'ex-vinyl',tags:['music'],u:'vihaan',likes:630,cm:[],liked:0},
 {seed:'ex-ghat',tags:['city','travel'],u:'sneha',likes:1450,cm:[],liked:0},
 {seed:'ex-court',tags:['sport'],u:'tanya',likes:720,cm:[],liked:0},
 {seed:'ex-bloom',tags:['nature'],u:'leaf',likes:2380,cm:[],liked:0,tall:1},
 {seed:'ex-rooftop',tags:['city','night'],u:'kabir',likes:1670,cm:[],liked:0},
 {seed:'ex-classic',tags:['car'],u:'vihaan',likes:940,cm:[],liked:0},
 {seed:'ex-fog',tags:['nature','travel'],u:'sneha',likes:1250,cm:[],liked:0},
];
const chats=[
 {u:'sneha',unread:2,msgs:[{f:'them',t:'Bhai kal ka plan pakka na?',tm:'10:02'},{f:'me',t:'Pakka. 6 baje nikalenge',tm:'10:04'},{f:'them',t:'Tripod le lena, sunset shoot karna hai',tm:'10:05'}]},
 {u:'kabir',unread:1,msgs:[{f:'me',t:'Reel edit ho gayi?',tm:'9:04'},{f:'them',t:'Haan bas audio adjust karna hai',tm:'9:10'},{f:'them',t:'Dekh ke batana',tm:'9:12'}]},
 {u:'vihaan',msgs:[{f:'them',t:'Bhai wo wali meme dekhi?',tm:'8:30'},{f:'me',t:'LOL forward kar',tm:'8:32'},{f:'them',t:'College group mein daal di hai',tm:'8:33'}]},
 {u:'tanya',msgs:[{f:'them',t:'Practice video bheji hai, dekhna',tm:'Yest'},{f:'me',t:'Dekh liya, kill ho gayi',tm:'Yest'},{f:'them',t:'Thankyou thanyou',tm:'Yest'}]},
 {u:'dfr',msgs:[{f:'them',t:'Is weekend ka new reel live hai',tm:'Tue'},{f:'them',t:'Butter chicken wala dekha?',tm:'Tue'}]},
 {u:'ananya',msgs:[{f:'me',t:'Mural wali post bahut achi lagi',tm:'Mon'},{f:'them',t:'Thanks yaar! Next week naya wall hai',tm:'Mon'}]},
];
const acts=[
 {g:'Aaj'},
 {t:'like',u:'tanya',when:'2h',thumb:ph('ig-mural',120)},
 {t:'follow',u:'leaf',when:'4h'},
 {g:'Is hafte'},
 {t:'req',u:'vihaan',when:'1d'},
 {t:'like',u:'sneha',when:'2d',thumb:ph('ig-sunrise',120)},
 {t:'comment',u:'rohan',when:'2d',txt:'"frame hi alag hai"',thumb:ph('ig-butter',120)},
 {t:'mention',u:'kabir',when:'3d',txt:'reel mein',thumb:ph('rl-kabir',120)},
 {g:'Is mahine'},
 {t:'follow',u:'dfr',when:'2w'},
 {t:'like',u:'ananya',when:'3w',thumb:ph('ex-mural',120)},
];
const NOTES=[{u:'kabir',t:'Reel bana raha hu'},{u:'tanya',t:'Practice at 6'},{u:'vihaan',t:'kab milenge?'},{u:'sneha',t:'Trip kal hai!'}];
const REPL=['Hahaha sahi mein','Achha theek hai, done','Sun kal milte hain phir dekhte hain','Reel ka link bhej na jaldi','Chal baad mein baat karte hain','Haan bilkul!','Arey wah kya baat','Hmm sochke batata hu','2 min, photo bhej raha hu','LOL ekdum','Yaar ye toh bhool gaya tha'];
const TABS=['feed','explore','reels','profile'];
function go(id){
 $$('.screen').forEach(s=>s.classList.toggle('on',s.id==='scr-'+id));
 $('#bnav').style.display=TABS.includes(id)?'flex':'none';
 $$('.bnav [data-go]').forEach(b=>b.classList.toggle('on',b.dataset.go===id));
 hideSheets();
 if(id==='reels'){initReels();requestAnimationFrame(playVisibleReels)}else pauseVideos();
 if(id==='profile')statUp();
 if(id==='activity'){actUnread=0;updateBadges()}
 if(id==='messages'){chats.forEach(c=>c.unread=0);renderChatList();updateBadges()}
}
document.addEventListener('click',e=>{const b=e.target.closest('[data-back]');if(b)go(b.dataset.back)});
 $('#bnav').addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.id==='nav-create'){openCreate('post');return}
 if(b.dataset.go)go(b.dataset.go);
});
let toastT;
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('on'),1900)}
function copyTxt(s){
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(s).then(()=>toast('Copy ho gaya')).catch(()=>toast(s));
 else toast(s);
}
let menuItems=[];
function menu(items){menuItems=items;$('#menu-list').innerHTML=items.map((it,i)=>`<button class="mn ${it.d?'danger':''}" data-mn="${i}">${it.l}</button>`).join('');openSheet('#sh-menu')}
 $('#sh-menu').addEventListener('click',e=>{const b=e.target.closest('[data-mn]');if(!b)return;const it=menuItems[+b.dataset.mn];hideSheets();it.f&&it.f()});
function openSheet(id){$('#veil').classList.add('on');$(id).classList.add('up')}
function hideSheets(){$$('.sheet').forEach(s=>s.classList.remove('up'));$('#veil').classList.remove('on')}
 $('#veil').addEventListener('click',hideSheets);
[['#shr-x'],['#cm-x'],['#cr-x'],['#ed-x']].forEach(([s])=>$(s).addEventListener('click',hideSheets));
const postById=id=>posts.find(p=>p.id===id);
function pavInner(u){const s=stories.find(x=>x.u===u);
 if(s&&s.items.length&&!s.seen)return `<span class="ring"><span class="in"><img src="${U[u].av}" alt=""></span></span>`;
 return `<span class="avw"><img src="${U[u].av}" alt=""></span>`}
function buildPost(p){const u=U[p.u];
 return `<article class="post" data-pid="${p.id}">
  <header class="p-hd">
   <button class="p-av" data-pav="${p.u}">${pavInner(p.u)}</button>
   <span><span class="p-handle">${u.h}${u.v?ic('verified','vbadge'):''}</span> <span class="pd">·</span> <span class="p-time">${p.t}</span></span>
   ${p.u!=='you'&&!u.followed?`<button class="flw" data-follow="${p.u}">Follow</button>`:''}
   <button class="ib ml-auto" data-menu="${p.id}">${ic('ellipsis')}</button>
  </header>
  <div class="p-img"><img src="${p.img}" alt="" loading="lazy"><div class="burst">${ic('heart')}</div></div>
  <div class="p-act">
   <button class="ib likebtn ${p.liked?'on':''}" data-like="${p.id}">${ic('heart')}</button>
   <button class="ib" data-cm="${p.id}">${ic('comment')}</button>
   <button class="ib" data-share="${p.id}">${ic('plane')}</button>
   <button class="ib savebtn ml-auto ${p.saved?'on':''}" data-save="${p.id}">${ic('bookmark')}</button>
  </div>
  <div class="p-likes" data-likes="${p.id}">${fmt(p.likes)} likes</div>
  <div class="p-cap clamped"><b>${u.h}</b> ${esc(p.cap)}</div>
  <button class="p-cm" data-cm="${p.id}">View all ${p.cm.length} comments</button>
 </article>`;
}
function renderFeed(){$('#feed').innerHTML=posts.map(buildPost).join('')}
function renderStories(){$('#stories').innerHTML=stories.map((s,i)=>{
 const mine=s.u==='you',has=s.items.length;
 const ring=has&&!s.seen?'ring':'ring seen';
 return `<button class="st-it" data-story="${i}">
  <span class="${ring}"><span class="in"><img src="${U[s.u].av}" alt=""></span></span>
  ${mine&&!has?`<span class="st-plus">${ic('plusS')}</span>`:''}
  <span class="st-nm">${mine?'Your story':U[s.u].h}</span></button>`}).join('')}
function updLikeUI(pid){const p=postById(pid);const art=$(`[data-pid="${pid}"]`);
 art.querySelector('[data-like]').classList.toggle('on',p.liked);
 art.querySelector('[data-likes]').textContent=fmt(p.likes)+' likes'}
function likeOn(pid,burstIt){const p=postById(pid);if(!p.liked){p.liked=true;p.likes++}
 const art=$(`[data-pid="${pid}"]`);updLikeUI(pid);
 const b=art.querySelector('.likebtn');b.classList.remove('pop');void b.offsetWidth;b.classList.add('pop');
 if(burstIt){const bu=art.querySelector('.burst');bu.classList.remove('go');void bu.offsetWidth;bu.classList.add('go')}}
function toggleLike(pid){const p=postById(pid);p.liked=!p.liked;p.likes+=p.liked?1:-1;updLikeUI(pid)}
function toggleSave(pid){const p=postById(pid);p.saved=!p.saved;
 $(`[data-pid="${pid}"] [data-save]`).classList.toggle('on',p.saved);
 toast(p.saved?'Save ho gaya':'Saved se hata diya')}
function toggleFollow(uid){const u=U[uid];u.followed=!u.followed;
 $$(`[data-follow="${uid}"]`).forEach(b=>{b.textContent=u.followed?'Following':'Follow'});
 toast(u.followed?`@${u.h} ko follow kar diya`:`@${u.h} ko unfollow kar diya`)}
function dblTap(el){const n=Date.now();if(el._lt&&n-el._lt<330){el._lt=0;return true}el._lt=n;return false}
 $('#scr-feed').addEventListener('click',e=>{
 const t=s=>e.target.closest(s);let el;
 if(el=t('.p-img')){if(dblTap(el))likeOn(el.closest('.post').dataset.pid,true);return}
 if(el=t('[data-like]')){toggleLike(el.dataset.like);return}
 if(el=t('[data-save]')){toggleSave(el.dataset.save);return}
 if(el=t('.p-cap')){el.classList.toggle('clamped');return}
 if(el=t('[data-cm]')){openComments({type:'post',obj:postById(el.dataset.cm)});return}
 if(el=t('[data-share]')){const p=postById(el.dataset.share);openShare({img:p.img,text:p.cap});return}
 if(el=t('[data-follow]')){toggleFollow(el.dataset.follow);return}
 if(el=t('[data-pav]')){const uid=el.dataset.pav;const i=stories.findIndex(s=>s.u===uid);
  if(uid==='you'&&!(stories[0].items.length)){openCreate('story')}else if(i>-1)openStory(i);return}
 if(el=t('[data-menu]')){const pid=el.dataset.menu;const p=postById(pid);
  const items=[{l:'Copy link',f:()=>copyTxt('instagram.com/p/'+pid)},
        {l:'Share to…',f:()=>openShare({img:p.img,text:p.cap})},
        {l:'About this account',f:()=>toast('Ye account 2021 se Instagram par hai')}];
  if(p.u==='you')items.push({l:'Delete post',d:1,f:()=>{
    const i2=posts.indexOf(p);if(i2>-1)posts.splice(i2,1);
    const art=$(`[data-pid="${pid}"]`);if(art)art.remove();
    toast('Post delete ho gayi')}});
  items.push({l:'Cancel'});
  menu(items);return}
 if(el=t('[data-story]')){const i=+el.dataset.story,s=stories[i];
  if(s.u==='you'&&!s.items.length)openCreate('story');else openStory(i);return}
 if(t('#hb-act')){go('activity');return}
 if(t('#hb-dm')){go('messages');return}
});
 $('#scr-feed').addEventListener('scroll',function(){const y=this.scrollTop;$('#feed-hd').classList.toggle('hid',y>72&&y>feedLast);feedLast=y},{passive:true});
let feedLast=0;
let cmTarget=null;
function openComments(target){cmTarget=target;if(!cmTarget.obj.cm)cmTarget.obj.cm=[];renderCmList();openSheet('#sh-cm')}
function renderCmList(){$('#cm-list').innerHTML=cmTarget.obj.cm.map(c=>`
 <div class="cm-r">${avImg(c.u)}<div><b>${U[c.u].h}</b>${esc(c.t)}<div class="ct">${c.tm||''}</div></div></div>`).join('')||'<div class="ex-empty">Abhi koi comment nahi<br>Pehla comment tum karo</div>'}
function addComment(){const inp=$('#cm-inp');const t=inp.value.trim();if(!t||!cmTarget)return;
 cmTarget.obj.cm.push({u:'you',t,tm:'Abhi'});inp.value='';renderCmList();
 if(cmTarget.type==='post'){const p=cmTarget.obj;$(`[data-pid="${p.id}"] .p-cm`).textContent=`View all ${p.cm.length} comments`}
 else if(cmTarget.type==='reel'){const r=cmTarget.obj;r.cmN++;const sp=$(`[data-rid="${r.id}"] [data-rcm] span`);if(sp)sp.textContent=kfmt(r.cmN)}
 else if(cmTarget.type==='exp'&&$('#pv').classList.contains('on')){$('#pv-likes').textContent=fmt(cmTarget.obj.likes)+' likes · '+cmTarget.obj.cm.length+' comments'}
}
 $('#cm-post').addEventListener('click',addComment);
 $('#cm-inp').addEventListener('keydown',e=>{if(e.key==='Enter')addComment()});
let sharePayload=null,shareMode='share';
function openShare(payload){sharePayload=payload;shareMode='share';renderShare();openSheet('#sh-share')}
function renderShare(){
 $('#shr-title').textContent=shareMode==='new'?'New message':'Share';
 $('#shr-list').innerHTML=chats.map(c=>`
  <div class="shr-r" ${shareMode==='new'?`data-newchat="${c.u}"`:''}>
   <span class="shr-avw">${avImg(c.u)}${U[c.u].online?'<i class="on-dot"></i>':''}</span>
   <span class="shr-n">${U[c.u].n}<small>@${U[c.u].h}</small></span>
   ${shareMode==='share'?`<button class="shr-send" data-shrto="${c.u}">Send</button>`:`<span class="shr-chev">${ic('chev')}</span>`}
  </div>`).join('');
}
 $('#sh-share').addEventListener('click',e=>{
 const s=e.target.closest('[data-shrto]');
 if(s){pushTo(s.dataset.shrto,{img:sharePayload.img,t:sharePayload.text||''});toast(`@${U[s.dataset.shrto].h} ko bhej diya`);hideSheets();return}
 const n=e.target.closest('[data-newchat]');
 if(n){hideSheets();openChat(n.dataset.newchat)}
});
 $('#shr-x').addEventListener('click',hideSheets);
 $('#dm-new').addEventListener('click',()=>{shareMode='new';renderShare();openSheet('#sh-share')});
let chatWith=null,botT1,botT2;
const chatOf=u=>chats.find(c=>c.u===u)||(chats.unshift({u,msgs:[]}),chats[0]);
function prevTxt(c){const m=c.msgs[c.msgs.length-1];
 if(!m)return'Say hi';
 const t=m.unsent?'You unsent a message'
  :m.img?(m.f==='me'?'You sent a photo':'Sent a photo')
  :m.heart?(m.f==='me'?'You sent a heart':'Sent a heart')
  :(m.f==='me'?'You: ':'')+m.t;
 return t+' · '+m.tm}
function renderChatList(){$('#chat-list').innerHTML=chats.map(c=>`
 <div class="ch-row" data-chat="${c.u}">
  <span class="ch-av">${avImg(c.u)}${U[c.u].online?'<i class="on-dot"></i>':''}</span>
  <span class="ch-mid"><b>${U[c.u].n}${U[c.u].v?ic('verified','vbadge'):''}</b>
  <span class="ch-prev ${c.unread?'un':''}">${esc(prevTxt(c))}</span></span>
  <button class="ib ch-cam" data-chatcam="${c.u}">${ic('camera')}</button>
 </div>`).join('')}
function renderNotes(){$('#notes').innerHTML=NOTES.map(n=>`
 <button class="note" data-note="${n.u}"><span class="note-b">${esc(n.t)}</span>${avImg(n.u)}<span class="nm">${U[n.u].h}</span></button>`).join('')}
function openChat(uid){chatWith=uid;const c=chatOf(uid);c.unread=0;
 renderChat();go('chat');renderChatList();updateBadges();sendBtnState()}
function mrow(m,i){
 if(m.unsent)return `<div class="mrow me"><span class="unsent">You unsent a message</span></div>`;
 let inner='';
 if(m.img)inner+=`<div class="bub imgb"><img src="${m.img}" alt=""></div>`;
 if(m.t)inner+=`<div class="bub">${esc(m.t)}</div>`;
 if(m.heart)inner+=`<div class="bub hb">${ic('heart')}</div>`;
 return `<div class="mrow ${m.f}" data-mi="${i}">${inner}</div>`}
function renderChat(){const c=chatOf(chatWith),u=U[chatWith];
 $('#ch-av').src=u.av;
 $('#ch-dot').hidden=!u.online;
 $('#ch-name').innerHTML=esc(u.n)+(u.v?ic('verified','vbadge'):'');
 $('#ch-stat').textContent=u.online?'Active now':'Active '+(u.lastSeen||'recently');
 $('#msgs').innerHTML=`<div class="intro"><span class="intro-av">${avImg(chatWith)}</span><b>${esc(u.n)}${u.v?ic('verified','vbadge'):''}</b><span class="iun">${u.h} · Instagram</span><button class="pbtn" id="intro-vp">View profile</button></div><div class="day">Aaj</div>`+c.msgs.map((m,i)=>mrow(m,i)).join('');
 scrollBottom()}
function scrollBottom(){const m=$('#msgs');m.scrollTop=m.scrollHeight}
function killTyping(){const t=$('#typing');if(t)t.remove()}
function pushTo(uid,m){const c=chatOf(uid);m.f='me';m.tm=nowT();c.msgs.push(m);
 if(uid===chatWith&&$('#scr-chat').classList.contains('on')){killTyping();$('#msgs').insertAdjacentHTML('beforeend',mrow(m,c.msgs.length-1));scrollBottom()}
 renderChatList()}
function botReply(){
 clearTimeout(botT1);clearTimeout(botT2);killTyping();
 botT1=setTimeout(()=>{if($('#scr-chat').classList.contains('on')){$('#msgs').insertAdjacentHTML('beforeend','<div class="mrow them" id="typing"><div class="bub"><i></i><i></i><i></i></div></div>');scrollBottom()}},650);
 botT2=setTimeout(()=>{killTyping();const c=chatOf(chatWith);
  const t=REPL[Math.floor(Math.random()*REPL.length)];c.msgs.push({f:'them',t,tm:nowT()});
  if($('#scr-chat').classList.contains('on')){$('#msgs').insertAdjacentHTML('beforeend',mrow(c.msgs[c.msgs.length-1],c.msgs.length-1));scrollBottom()}
  else{c.unread=(c.unread||0)+1;updateBadges()}
  renderChatList()},1600+Math.random()*1200);
}
function sendBtnState(){const has=$('#chat-inp').value.trim().length>0;
 $('#chat-r').style.display=has?'none':'flex';
 $('#chat-send').hidden=!has}
function sendTxt(){const inp=$('#chat-inp');const t=inp.value.trim();if(!t)return;
 inp.value='';sendBtnState();pushTo(chatWith,{t});botReply()}
 $('#chat-inp').addEventListener('input',sendBtnState);
 $('#chat-inp').addEventListener('keydown',e=>{if(e.key==='Enter')sendTxt()});
 $('#chat-send').addEventListener('click',sendTxt);
 $('#chat-heart').addEventListener('click',()=>{pushTo(chatWith,{heart:true});botReply()});
 $('#chat-mic').addEventListener('click',()=>toast('Voice note demo mein off hai'));
 $('#chat-img').addEventListener('click',()=>{camTarget=chatWith;$('#chat-file').click()});
 $('#chat-smile').addEventListener('click',()=>{const e=['😂','🔥','❤️','👀','🙌'];$('#chat-inp').value+=e[Math.floor(Math.random()*e.length)];sendBtnState();$('#chat-inp').focus()});
 $$('#scr-chat [data-call]').forEach(b=>b.addEventListener('click',()=>toast(U[chatWith].n+' ko call lag rahe hain… (demo)')));
 $('#msgs').addEventListener('click',e=>{
 if(e.target.closest('#intro-vp')){toast('Profile view (demo)');return}
 const r=e.target.closest('.mrow');if(!r||r.dataset.mi===undefined)return;
 const c=chatOf(chatWith);const m=c.msgs[+r.dataset.mi];
 if(!m||m.unsent)return;
 if(m.f!=='me'){menu([{l:'Copy',f:()=>copyTxt(m.t||'')},{l:'Cancel'}]);return}
 menu([{l:'Copy',f:()=>copyTxt(m.t||'Photo')},
  {l:'Unsend',d:1,f:()=>{m.unsent=true;delete m.t;delete m.img;delete m.heart;
   renderChat();renderChatList();toast('Message unsend ho gaya')}},
  {l:'Cancel'}]);
});
 $('#chat-list').addEventListener('click',e=>{
 const cam=e.target.closest('[data-chatcam]');
 if(cam){camTarget=cam.dataset.chatcam;$('#chat-file').click();return}
 const r=e.target.closest('[data-chat]');if(r)openChat(r.dataset.chat)});
 $('#notes').addEventListener('click',e=>{const n=e.target.closest('[data-note]');if(n)openChat(n.dataset.note)});
 $('#req-row').addEventListener('click',()=>toast('Koi follow request pending nahi hai'));
 $('#dm-q').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();
 $$('#chat-list .ch-row').forEach(r=>{const u=U[r.dataset.chat];
  r.style.display=(u.n+' '+u.h).toLowerCase().includes(q)?'':'none'})});
let camTarget=null;
 $('#chat-cam').addEventListener('click',()=>{camTarget=chatWith;$('#chat-file').click()});
 $('#chat-file').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;
 const rd=new FileReader();rd.onload=()=>{pushTo(camTarget,{img:rd.result});if(camTarget===chatWith)botReply()};rd.readAsDataURL(f);e.target.value=''});
let actUnread=3;
function updateBadges(){const un=chats.reduce((a,c)=>a+(c.unread||0),0);
 const bd=$('#bdg-dm');bd.textContent=un;bd.style.display=un?'flex':'none';
 const ba=$('#bdg-act');ba.textContent=actUnread;ba.style.display=actUnread?'flex':'none'}
function buildExplore(){$('#ex-grid').innerHTML=explore.map((o,i)=>`
 <button class="tile ${o.tall?'tall':''}" data-ex="${i}"><img src="${ph(o.seed,600,o.tall?1100:600)}" alt="" loading="lazy"></button>`).join('')}
 $('#ex-grid').addEventListener('click',e=>{const t=e.target.closest('[data-ex]');if(t)openPhoto(explore[+t.dataset.ex],true)});
 $('#ex-q').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();
 $('#ex-clear').hidden=!q;let n=0;
 $$('#ex-grid .tile').forEach((tile,i)=>{const o=explore[i];
  const hay=o.tags.join(' ')+' '+U[o.u].h+' '+U[o.u].n;
  const show=!q||hay.toLowerCase().includes(q);
  tile.style.display=show?'':'none';if(show)n++});
 $('#ex-empty').hidden=n>0});
 $('#ex-clear').addEventListener('click',()=>{$('#ex-q').value='';$('#ex-q').dispatchEvent(new Event('input'))});
let pvObj=null;
function openPhoto(o,isExp){pvObj={o,isExp};
 $('#pv-img').src=isExp?ph(o.seed,900,1200):(o.full||o.img);
 $('#pv-av').src=U[o.u].av;
 $('#pv-user').innerHTML=U[o.u].h+(U[o.u].v?ic('verified','vbadge'):'');
 $('#pv-like').innerHTML=ic('heart');$('#pv-cm').innerHTML=ic('comment');$('#pv-share').innerHTML=ic('plane');
 $('#pv-like').classList.toggle('on',!!o.liked);
 $('#pv-likes').textContent=fmt(o.likes||0)+' likes'+(o.cm&&o.cm.length?' · '+o.cm.length+' comments':'');
 $('#pv').classList.add('on')}
 $('#pv-x').addEventListener('click',()=>$('#pv').classList.remove('on'));
 $('#pv-like').addEventListener('click',()=>{const o=pvObj.o;o.liked=!o.liked;o.likes+=o.liked?1:-1;
 $('#pv-like').classList.toggle('on',o.liked);
 $('#pv-likes').textContent=fmt(o.likes)+' likes'+(o.cm&&o.cm.length?' · '+o.cm.length+' comments':'')});
 $('#pv-cm').addEventListener('click',()=>{if(!pvObj.o.cm)pvObj.o.cm=[];openComments({type:'exp',obj:pvObj.o})});
 $('#pv-share').addEventListener('click',()=>openShare({img:$('#pv-img').src,text:pvObj.o.cap||''}));
let reelsReady=false,reelIO=null,reelsMuted=true;
function initReels(){if(reelsReady)return;reelsReady=true;
 $('#rscroll').innerHTML=reels.map(r=>`
 <section class="reel" data-rid="${r.id}">
  <video src="${r.vid}" poster="${r.poster}" ${reelsMuted?'muted':''} loop playsinline preload="metadata"></video>
  <div class="r-tap"></div>
  <div class="r-flash"></div>
  <div class="burst">${ic('heart')}</div>
  <div class="r-scrim"></div>
  <div class="r-info">
   <div class="r-user">${avImg(r.u)}<b>${U[r.u].h}</b><button class="r-flw ${U[r.u].followed?'fed':''}" data-rfollow="${r.u}">${U[r.u].followed?'Following':'Follow'}</button></div>
   <div class="r-cap">${esc(r.cap)}</div>
   <div class="r-music">${ic('music')}<div class="marq"><span>${esc(r.music)}&nbsp;&nbsp;·&nbsp;&nbsp;${esc(r.music)}&nbsp;&nbsp;·&nbsp;&nbsp;</span></div></div>
  </div>
  <div class="r-rail">
   <button class="rr likebtn ${r.liked?'on':''}" data-rlike="${r.id}">${ic('heart')}<span>${kfmt(r.likes)}</span></button>
   <button class="rr" data-rcm="${r.id}">${ic('comment')}<span>${kfmt(r.cmN)}</span></button>
   <button class="rr" data-rshare="${r.id}">${ic('plane')}</button>
   <button class="rr" data-rmenu="${r.id}">${ic('ellipsis')}</button>
   <div class="rr-disc">${avImg(r.u)}</div>
  </div>
 </section>`).join('');
 reelIO=new IntersectionObserver(es=>es.forEach(en=>{
  const v=en.target.querySelector('video');
  if(en.isIntersecting)v.play().catch(()=>{});else v.pause();
 }),{root:$('#rscroll'),threshold:.65});
 $$('#rscroll .reel').forEach(r=>reelIO.observe(r));
 setMuteUI();
}
function setMuteUI(){$('#reels-mute').innerHTML=ic(reelsMuted?'volx':'vol');
 $$('#rscroll video').forEach(v=>v.muted=reelsMuted)}
 $('#reels-mute').addEventListener('click',()=>{reelsMuted=!reelsMuted;setMuteUI()});
function pauseVideos(){$$('#rscroll video').forEach(v=>v.pause())}
function playVisibleReels(){if(!reelsReady)return;const rs=$('#rscroll'),h=rs.clientHeight,st=rs.scrollTop;
 $$('#rscroll .reel').forEach(r=>{const v=r.querySelector('video');const c=r.offsetTop+r.offsetHeight/2;
  if(c>st&&c<st+h)v.play().catch(()=>{});else v.pause()})}
function flash(reel,name){const f=reel.querySelector('.r-flash');f.innerHTML=ic(name);
 f.classList.remove('go');void f.offsetWidth;f.classList.add('go')}
function reelLike(r,burstIt){if(!r.liked){r.liked=true;r.likes++}
 const reel=$(`[data-rid="${r.id}"]`);const b=reel.querySelector('[data-rlike]');
 b.classList.toggle('on',r.liked);b.querySelector('span').textContent=kfmt(r.likes);
 if(burstIt){const bu=reel.querySelector('.burst');bu.classList.remove('go');void bu.offsetWidth;bu.classList.add('go')}}
 $('#scr-reels').addEventListener('click',e=>{
 const t=s=>e.target.closest(s);let el;
 if(el=t('.r-tap')){const reel=el.closest('.reel');const v=reel.querySelector('video');
  const d=dblTap(el);
  if(v.paused)v.play().catch(()=>{});else v.pause();
  flash(reel,v.paused?'play':'pause');
  if(d)reelLike(reels.find(x=>x.id===reel.dataset.rid),true);return}
 if(el=t('[data-rlike]')){reelLike(reels.find(x=>x.id===el.dataset.rlike));return}
 if(el=t('[data-rcm]')){const r=reels.find(x=>x.id===el.dataset.rcm);openComments({type:'reel',obj:r});return}
 if(el=t('[data-rshare]')){const r=reels.find(x=>x.id===el.dataset.rshare);openShare({img:r.poster,text:r.cap});return}
 if(el=t('[data-rfollow]')){const uid=el.dataset.rfollow;toggleFollow(uid);
  $$(`[data-rfollow="${uid}"]`).forEach(b=>{b.textContent=U[uid].followed?'Following':'Follow';b.classList.toggle('fed',U[uid].followed)});return}
 if(el=t('[data-rmenu]')){menu([{l:'Copy link',f:()=>copyTxt('instagram.com/reels/'+el.dataset.rmenu)},
  {l:'Not interested',f:()=>toast('Theek hai, aisa content kam dikhega')},{l:'Cancel'}])}
});
function renderAct(){$('#act-list').innerHTML=acts.map(a=>{
 if(a.g)return `<div class="act-g">${a.g}</div>`;
 const u=U[a.u];
 const mini=a.t==='like'?'<span class="mini red">'+ic('heart')+'</span>'
  :(a.t==='follow'||a.t==='req')?'<span class="mini blue">'+ic('user')+'</span>'
  :'<span class="mini blue">'+ic('comment')+'</span>';
 const tx=a.t==='like'?`<b>${u.h}</b> ne aapki post like ki.`
  :a.t==='follow'?`<b>${u.h}</b> ne aapko follow karna shuru kiya.`
  :a.t==='req'?`<b>${u.h}</b> aapko follow karna chahte hain.`
  :a.t==='comment'?`<b>${u.h}</b> ne comment kiya: ${esc(a.txt)}`
  :`<b>${u.h}</b> ne aapko ek ${esc(a.txt)} mein mention kiya.`;
 const right=a.thumb?`<img class="act-thumb" src="${a.thumb}" alt="">`
  :a.t==='follow'?`<button class="afb ${u.followed?'fed':''}" data-afollow="${a.u}">${u.followed?'Following':'Follow'}</button>`
  :a.t==='req'?`<span class="req-btns"><button class="afb" data-confirm>Confirm</button><button class="afb ghost" data-delrow>Delete</button></span>`:'';
 return `<div class="act-r"><span class="act-av">${avImg(a.u)}${mini}</span><span class="act-tx">${tx} <span class="tm">${a.when}</span></span>${right}</div>`;
}).join('')}
 $('#act-list').addEventListener('click',e=>{
 const f=e.target.closest('[data-afollow]');
 if(f){const uid=f.dataset.afollow;U[uid].followed=!U[uid].followed;
  f.textContent=U[uid].followed?'Following':'Follow';f.classList.toggle('fed',U[uid].followed);return}
 const c=e.target.closest('[data-confirm]');
 if(c){c.closest('.req-btns').outerHTML='<button class="afb fed">Following</button>';toast('Request confirm ho gayi');return}
 const d=e.target.closest('[data-delrow]');
 if(d){const row=d.closest('.act-r');row.remove();toast('Request delete ho gayi')}
});
let statsDone=false;
function statUp(){if(statsDone)return;statsDone=true;
 [['st-posts',12],['st-followers',8462],['st-following',431]].forEach(([id,target])=>{
  const el=document.getElementById(id),t0=performance.now();
  (function f(t){const p=Math.min(1,(t-t0)/900),e2=1-Math.pow(1-p,3);
   el.textContent=Math.round(target*e2).toLocaleString('en-IN');
   if(p<1)requestAnimationFrame(f)})(t0)})}
function renderPfAv(){$('#pf-av').innerHTML=stories[0].items.length&&!stories[0].seen
 ?`<span class="ring"><span class="in"><img src="${U.you.av}" alt=""></span></span>`
 :`<span class="ring seen"><span class="in"><img src="${U.you.av}" alt=""></span></span>`;
 $('#nav-pav img').src=U.you.av}
function renderHls(){$('#pf-hls').innerHTML=[['Ladakh','hl-ladakh'],['Street Food','hl-food'],['2024','hl-24'],['Desk Setup','hl-desk']]
 .map(([l,s])=>`<button class="hl" data-hl="${s}"><span class="hlc"><img src="${ph(s,160)}" alt=""></span>${l}</button>`).join('')}
 $('#pf-hls').addEventListener('click',e=>{const b=e.target.closest('[data-hl]');if(!b)return;
 openPhoto({u:'you',likes:312,liked:0,cm:[],img:ph(b.dataset.hl,900,1125),full:ph(b.dataset.hl,900,1125)})});
function renderPfGrid(tab){const g=$('#pf-grid');
 if(tab==='posts')g.innerHTML=Array.from({length:12},(_,i)=>`<div class="pf-t"><img src="${ph('pg'+(i+1),500)}" alt="" loading="lazy"></div>`).join('');
 else if(tab==='reels'){const views=['128K','45.7K','89.2K','12.4K','67.1K','23.9K'];
  g.innerHTML=Array.from({length:6},(_,i)=>`<div class="pf-t rvw"><img src="${ph('pr'+(i+1),500)}" alt="" loading="lazy"><span class="rv">${ic('play')}${views[i]}</span></div>`).join('')}
 else g.innerHTML=['tg1','tg2','tg3'].map(s=>`<div class="pf-t"><img src="${ph(s,500)}" alt="" loading="lazy"></div>`).join('')}
 $('#pf-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-tab]');if(!b)return;
 $$('#pf-tabs button').forEach(x=>x.classList.toggle('on',x===b));renderPfGrid(b.dataset.tab)});
 $('#pf-add').addEventListener('click',()=>openCreate('post'));
 $('#pf-menu').addEventListener('click',()=>menu([
 {l:'Saved',f:()=>{go('saved');renderSaved()}},
 {l:'Copy profile link',f:()=>copyTxt('instagram.com/aarav_wanders')},
 {l:'Cancel'}]));
 $('#pf-link').addEventListener('click',()=>copyTxt('https://bit.ly/aarav-films'));
 $('#pf-share').addEventListener('click',()=>openShare({text:'Profile: @aarav_wanders'}));
 $('#pf-edit').addEventListener('click',()=>{$('#ed-name').value=U.you.n;$('#ed-bio').value=$('#pf-bio').innerText.trim();openSheet('#sh-edit')});
 $('#ed-save').addEventListener('click',()=>{const n=$('#ed-name').value.trim();if(n)U.you.n=n;$('#pf-name').textContent=n||U.you.n;
 $('#pf-bio').innerText=$('#ed-bio').value.trim()||$('#pf-bio').innerText;hideSheets();toast('Profile update ho gaya')});
function renderSaved(){const saved=posts.filter(p=>p.saved);
 $('#sv-grid').innerHTML=saved.map(p=>`<button class="tile" data-sv="${p.id}"><img src="${p.img}" alt=""></button>`).join('');
 $('#sv-empty').hidden=saved.length>0;$('#sv-grid').style.display=saved.length?'grid':'none'}
 $('#sv-grid').addEventListener('click',e=>{const t=e.target.closest('[data-sv]');if(!t)return;
 const p=postById(t.dataset.sv);openPhoto({u:p.u,likes:p.likes,liked:p.liked,cm:p.cm,img:p.img,full:p.img})});
let crSel=null,crMode='post',crStage=1;
function buildCrGrid(){
 let html=`<button class="cr-t cr-up" id="cr-up">${ic('camera')}Upload</button>`;
 for(let i=1;i<=12;i++)html+=`<button class="cr-t" data-crsrc="${ph('cr'+i,900,1125)}"><img src="${ph('cr'+i,400,400)}" alt="" loading="lazy"></button>`;
 $('#cr-grid').innerHTML=html;
}
 $('#cr-grid').addEventListener('click',e=>{
 if(e.target.closest('#cr-up')){$('#cr-file').click();return}
 const t=e.target.closest('[data-crsrc]');if(!t)return;
 crSel=t.dataset.crsrc;crPicked()});
 $('#cr-file').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;
 const rd=new FileReader();rd.onload=()=>{crSel=rd.result;crPicked()};rd.readAsDataURL(f);e.target.value=''});
function crPicked(){$$('#cr-grid .cr-t').forEach(t2=>t2.classList.remove('sel'));
 $$('#cr-grid [data-crsrc]').forEach(t2=>{if(t2.dataset.crsrc===crSel)t2.classList.add('sel')});
 $('#cr-next').disabled=false}
function openCreate(mode){crMode=mode;crSel=null;crStage=1;
 $('#cr-title').textContent=mode==='story'?'Add to story':'New post';
 $('#cr-next').textContent='Next';$('#cr-next').disabled=true;
 $('#cr-step1').hidden=false;$('#cr-step2').hidden=true;
 $$('#cr-grid .cr-t').forEach(t2=>t2.classList.remove('sel'));
 $('#cr-cap').value='';openSheet('#sh-create')}
 $('#cr-next').addEventListener('click',()=>{
 if(!crSel)return;
 if(crStage===1){$('#cr-img').src=crSel;$('#cr-step1').hidden=true;$('#cr-step2').hidden=false;
  $('#cr-next').textContent='Share';crStage=2}
 else publish()});
function publish(){
 const cap=$('#cr-cap').value.trim();
 posts.unshift({id:'me'+Date.now(),u:'you',img:crSel,likes:0,liked:0,saved:0,t:'Abhi',cap,cm:[]});
 $('#feed').insertAdjacentHTML('afterbegin',buildPost(posts[0]));
 $('#feed').firstElementChild.classList.add('new');
 hideSheets();go('feed');$('#scr-feed').scrollTop=0;
 if(crMode==='story'){stories[0].items.push({img:crSel,t:'Abhi'});stories[0].seen=false;
  renderStories();renderPfAv();toast('Story add ho gayi')}
 else toast('Post share ho gayi');
}
const sv={open:false,ui:0,ii:0,prog:0,hold:false,last:0};
function openStory(i){sv.open=true;sv.ui=i;sv.ii=0;
 $('#sv').classList.add('on');svBuildSegs();svShow();
 sv.last=performance.now();requestAnimationFrame(svTick)}
function svBuildSegs(){const s=stories[sv.ui];
 $('#sv-segs').innerHTML=s.items.map(()=>'<i><b></b></i>').join('');
 $('#sv-av').innerHTML=avImg(s.u);
 $('#sv-name').textContent=s.u==='you'?'Your story':U[s.u].h}
function svShow(){const s=stories[sv.ui],it=s.items[sv.ii];sv.prog=0;
 const img=$('#sv-img');img.classList.remove('kb');img.src=it.img;void img.offsetWidth;img.classList.add('kb');
 $('#sv-time').textContent=it.t;svPaint();
 const nx=s.items[sv.ii+1]||stories[sv.ui+1]&&stories[sv.ui+1].items[0];
 if(nx){const p=new Image();p.src=nx.img}}
function svPaint(){$$('#sv-segs b').forEach((b,i)=>{b.style.width=i<sv.ii?'100%':i===sv.ii?(sv.prog*100)+'%':'0%'})}
function svTick(ts){if(!sv.open)return;const dt=ts-sv.last;sv.last=ts;
 if(!sv.hold){sv.prog+=dt/5200;if(sv.prog>=1)svNext()}
 svPaint();requestAnimationFrame(svTick)}
function svNext(){const s=stories[sv.ui];
 if(sv.ii<s.items.length-1){sv.ii++;svShow()}
 else{stories[sv.ui].seen=true;
  if(sv.ui<stories.length-1){sv.ui++;sv.ii=0;svBuildSegs();svShow()}
  else closeStory()}}
function svPrev(){if(sv.ii>0){sv.ii--;svShow()}
 else if(sv.ui>0){stories[sv.ui].seen=true;sv.ui--;sv.ii=0;svBuildSegs();svShow()}
 else sv.prog=0}
function closeStory(){sv.open=false;$('#sv').classList.remove('on');renderStories();renderPfAv()}
let svPT=0;
function svZone(e){sv.hold=true;svPT=Date.now()}
function svZoneUp(e,zone){sv.hold=false;
 if(Date.now()-svPT<260){
  const rect=$('.phone').getBoundingClientRect();
  const frac=(e.clientX-rect.left)/rect.width;
  frac<.38?svPrev():svNext();
 }
}
['sv-prev','sv-next'].forEach(id=>{const z=document.getElementById(id);
 z.addEventListener('pointerdown',svZone);
 z.addEventListener('pointerup',e=>svZoneUp(e));
 z.addEventListener('pointerleave',()=>{sv.hold=false})});
 $('#sv-x').addEventListener('click',closeStory);
 $('#sv-like').addEventListener('click',()=>{$('#sv-like').classList.toggle('on')});
 $('#sv-share').addEventListener('click',()=>{const s=stories[sv.ui];
 openShare({img:s.items[sv.ii].img,text:'Story share ki'})});
 $('#sv-inp').addEventListener('keydown',e=>{if(e.key!=='Enter')return;
 const v=e.target.value.trim();if(!v)return;
 const uid=stories[sv.ui].u;
 if(uid==='you'){toast('Ye aapki apni story hai');e.target.value='';return}
 pushTo(uid,{t:v});toast('Reply bhej diya');e.target.value=''});
 $('#cm-av').src=U.you.av;
renderStories();renderFeed();buildExplore();renderNotes();renderChatList();renderAct();
renderPfAv();renderHls();renderPfGrid('posts');buildCrGrid();updateBadges();
</script>
</body>
</html>
"""

components.html(APP_HTML, height=940, scrolling=False)
