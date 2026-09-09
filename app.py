<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Zar — Share. Play. Earn.</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%2317b558'/%3E%3Cpath d='M23 23h18L23 41h18' stroke='%23fff' stroke-width='5' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --g1:#2fe56d;--g2:#17b558;--g3:#0e9147;--g4:#0a7c3d;--gdeep:#075c2d;
  --bg:#f4f7f4;--card:#ffffff;--tx:#14211a;--mut:#6d7d72;--line:#e3eae4;--soft:#eef4ef;
  --red:#e5484d;--amber:#df9a26;--tbb:rgba(244,247,244,.86);--pg:#dfe6df;
}
[data-theme=dark]{--bg:#0b110d;--card:#131b15;--tx:#e7efe9;--mut:#8ba394;--line:#202b23;--soft:#18231c;--tbb:rgba(11,17,13,.86);--pg:#050806}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{min-height:100%}
body{font-family:'Plus Jakarta Sans',system-ui,sans-serif;font-size:15px;color:var(--tx);background:var(--pg)}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
input,textarea,select{font:inherit;color:inherit}
img{display:block}
.ic{flex:none;display:block}
#app{max-width:480px;margin:0 auto;min-height:100dvh;background:var(--bg);position:relative;box-shadow:0 0 70px rgba(0,0,0,.14)}
.mcol{max-width:480px;margin:0 auto;min-height:100dvh;display:flex;flex-direction:column;position:relative}
.mut{color:var(--mut)}
b{font-weight:700}
/* ---------- SPLASH ---------- */
.splash{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff;position:relative;overflow:hidden;padding:32px;
  background:linear-gradient(178deg,#2fe56d 0%,#17b558 46%,#0a7c3d 100%)}
.splash::before{content:"";position:absolute;inset:-40%;background:repeating-linear-gradient(115deg,rgba(255,255,255,.055) 0 26px,transparent 26px 78px)}
.splash>*{position:relative}
.slogo{animation:float 3.4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.sname{font-family:Sora,sans-serif;font-weight:800;font-size:44px;letter-spacing:-1px;margin-top:18px}
.stag{opacity:.85;font-weight:500;margin-top:6px;letter-spacing:.4px}
.getstart{margin-top:auto;background:#fff;color:var(--g3);font-weight:800;font-size:16px;padding:16px 0;width:100%;max-width:340px;border-radius:999px;box-shadow:0 10px 30px rgba(0,40,15,.25);transition:transform .15s}
.getstart:active{transform:scale(.96)}
.haveacc{margin-top:16px;background:none;color:#fff;opacity:.92;font-weight:600;text-decoration:underline;text-underline-offset:4px}
/* ---------- AUTH ---------- */
.authbg{height:31dvh;min-height:210px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;position:relative;
  background:linear-gradient(180deg,#2fe56d,#17b558 55%,#0e9147)}
.authbg::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(255,255,255,.05) 0 24px,transparent 24px 72px)}
.authbg>*{position:relative}
.authbg .sname{font-size:30px;margin-top:10px}
.sheet{flex:1;background:var(--card);border-radius:30px 30px 0 0;margin-top:-30px;padding:28px 24px calc(30px + env(safe-area-inset-bottom));position:relative;z-index:2}
.sheet h2{font-family:Sora,sans-serif;font-weight:800;color:var(--g2);font-size:30px;letter-spacing:-.5px}
.sheet .sub{color:var(--mut);margin:4px 0 20px;font-weight:500}
.inp{display:flex;align-items:center;gap:11px;background:var(--soft);border:1.6px solid var(--line);border-radius:999px;padding:0 17px;height:50px;margin-bottom:12px;transition:border-color .15s}
.inp:focus-within{border-color:var(--g2)}
.inp input{flex:1;border:0;outline:0;background:transparent;min-width:0}
.inp .mut{color:var(--mut)}
.eye{color:var(--mut);padding:6px}
.btn{display:block;width:100%;background:var(--g2);color:#fff;font-weight:800;padding:15px;border-radius:999px;text-align:center;transition:transform .12s,filter .15s}
.btn:active{transform:scale(.97)}
.btn:disabled{filter:grayscale(.5);opacity:.7}
.btn.red{background:var(--red)}
.btn.ghost{background:var(--soft);color:var(--tx)}
.btnline{color:var(--g2);font-weight:700}
.divider{display:flex;align-items:center;gap:14px;color:var(--mut);font-size:13px;font-weight:600;margin:20px 0}
.socials{display:flex;justify-content:center;gap:16px;margin-bottom:20px}
.soc{width:52px;height:52px;border-radius:16px;display:flex;align-items:center;justify-content:center;border:1.5px solid var(--line);transition:transform .12s}
.soc:active{transform:scale(.92)}
.soc.gh{background:#fff}.soc.fb{background:#1877F2}.soc.ap{background:#111}
.terms{display:flex;gap:10px;align-items:flex-start;font-size:13px;color:var(--mut);margin:2px 0 16px;line-height:1.45}
.cb{width:20px;height:20px;border-radius:6px;border:1.8px solid var(--line);flex:none;margin-top:1px;display:flex;align-items:center;justify-content:center;color:#fff;transition:.15s}
.cb.on{background:var(--g2);border-color:var(--g2)}
.aerr{color:var(--red);font-size:13px;font-weight:600;margin:-4px 0 10px;min-height:17px}
.demolink{text-align:center;margin-top:18px;font-size:13px;font-weight:600;color:var(--mut)}
.smallnote{background:#fff8e6;border:1px solid #f2e2b3;color:#7a5b12;border-radius:12px;padding:10px 14px;font-size:13px;font-weight:600;margin-bottom:14px;line-height:1.5}
/* ---------- TOPBAR ---------- */
.tb{position:sticky;top:0;z-index:30;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 16px;background:var(--tbb);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.wordmark{font-family:Sora,sans-serif;font-weight:800;font-size:23px;color:var(--g2);letter-spacing:-.5px}
.tbtitle{font-family:Sora,sans-serif;font-weight:700;font-size:18px}
.tbacts{display:flex;gap:4px}
.tbacts button{padding:8px;position:relative;border-radius:12px}
.tbacts button:active{background:var(--soft)}
.dot{position:absolute;top:7px;right:7px;width:8px;height:8px;border-radius:50%;background:var(--red);border:2px solid var(--card)}
.icbtn.on svg{color:var(--red)}
.icbtn.on svg.f{fill:var(--red)}
.icbtn.save.on svg{color:var(--tx)}
.icbtn.save.on svg.f{fill:var(--tx)}
/* ---------- BOTTOM NAV (Instagram style) ---------- */
.nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:480px;height:calc(52px + env(safe-area-inset-bottom));background:var(--card);border-top:1px solid var(--line);display:flex;align-items:stretch;z-index:40;padding-bottom:env(safe-area-inset-bottom)}
.nav button{flex:1;display:flex;align-items:center;justify-content:center;color:#8b988e;position:relative;transition:color .15s}
.nav button.on{color:var(--tx)}
.nav button:active svg{transform:scale(.85)}
.nav .pav{width:27px;height:27px;border-radius:50%;border:2px solid transparent;object-fit:cover}
.nav button.on .pav{border-color:var(--tx)}
.nav .plusbtn svg{color:var(--g2)}
.nav .plusbtn.on{color:var(--g2)}
/* ---------- STORIES ---------- */
.strow{display:flex;gap:14px;overflow-x:auto;padding:6px 16px 12px;scrollbar-width:none}
.strow::-webkit-scrollbar{display:none}
.stit{display:flex;flex-direction:column;align-items:center;gap:5px;flex:none;width:66px}
.sring{width:62px;height:62px;border-radius:50%;padding:2.5px;background:conic-gradient(from 210deg,#2fe56d,#c4f6d6,#17b558,#0a7c3d,#2fe56d)}
.sring.seen{background:var(--line)}
.sring img{width:100%;height:100%;border-radius:50%;object-fit:cover;border:2.5px solid var(--card)}
.stit span{font-size:11.5px;color:var(--mut);max-width:66px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stit .plusov{position:absolute;right:-2px;bottom:12px;width:21px;height:21px;border-radius:50%;background:var(--g2);color:#fff;border:2.5px solid var(--card);display:flex;align-items:center;justify-content:center}
.livedot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--red);margin-right:6px;animation:pulse 1.2s infinite}
@keyframes pulse{50%{opacity:.35}}
.livechip{flex:none;display:flex;align-items:center;background:var(--card);border:1.5px solid var(--line);border-radius:999px;padding:8px 14px;font-weight:700;font-size:13px}
.livechip b{color:var(--red)}
/* ---------- POST CARD ---------- */
.pcard{background:var(--card);border-bottom:1px solid var(--line);padding-bottom:10px}
.phead{display:flex;align-items:center;gap:10px;padding:10px 14px}
.phead .nm{font-weight:700;font-size:14.5px;line-height:1.25}
.phead .sub{font-size:12.5px}
.av{width:38px;height:38px;border-radius:50%;object-fit:cover;flex:none}
.pmedia{position:relative;background:#000;cursor:pointer}
.pmedia img{width:100%;max-height:520px;object-fit:cover}
.bigh{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;opacity:0;pointer-events:none}
.bigh.go{animation:bigh .8s ease forwards}
@keyframes bigh{0%{opacity:0;transform:scale(.4)}25%{opacity:.95;transform:scale(1.15)}60%{opacity:.95;transform:scale(1)}100%{opacity:0;transform:scale(.9)}}
.pacts{display:flex;gap:6px;padding:8px 8px 0;align-items:center}
.pa{padding:7px;border-radius:10px}
.pa:active svg{transform:scale(.85)}
.pa.on svg{color:var(--red)}
.pa.on svg.f{fill:var(--red)}
.pa.save.on svg{color:var(--tx)}
.pa.save.on svg.f{fill:var(--tx)}
.pa:last-child{margin-left:auto}
.plikes{padding:5px 15px 0;font-weight:700;font-size:13.5px}
.pcap{padding:3px 15px 0;font-size:14px;line-height:1.45}
.htg{color:var(--g2);font-weight:700}
.pviewall{padding:4px 15px 0;color:var(--mut);font-size:13.5px;font-weight:600}
.pc2{padding:2px 15px 0;font-size:13.5px;color:var(--mut);line-height:1.5}
.pc2 b{color:var(--tx)}
.ptime{padding:4px 15px 2px;font-size:11.5px;color:var(--mut)}
.sechead{padding:14px 16px 8px;font-size:12px;font-weight:800;letter-spacing:1.2px;text-transform:uppercase;color:var(--mut)}
/* ---------- LISTS / SETTINGS ---------- */
.group{background:var(--card);border-radius:18px;margin:0 16px 18px;overflow:hidden;border:1px solid var(--line)}
.srow{display:flex;align-items:center;gap:13px;padding:14px 16px;border-bottom:1px solid var(--line);min-height:54px}
.srow:last-child{border-bottom:0}
.srow:active{background:var(--soft)}
.srow .ric{width:34px;height:34px;border-radius:10px;background:var(--soft);color:var(--g2);display:flex;align-items:center;justify-content:center;flex:none}
.srow .lbl{flex:1;min-width:0}
.srow .lbl b{font-weight:700;font-size:14.5px;display:block}
.srow .lbl span{font-size:12.5px;color:var(--mut);line-height:1.35;display:block}
.srow.red .ric{color:var(--red)}
.srow.red .lbl b{color:var(--red)}
.srow .rav{width:48px;height:48px}
.sw{width:46px;height:28px;border-radius:999px;background:var(--line);position:relative;transition:.2s;flex:none}
.sw i{position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;transition:.2s;box-shadow:0 1px 4px rgba(0,0,0,.25)}
.sw.on{background:var(--g2)}
.sw.on i{left:21px}
/* ---------- FEED EXTRAS ---------- */
.seg{display:flex;background:var(--soft);border-radius:999px;padding:4px;margin:4px 16px 12px}
.seg button{flex:1;padding:9px;border-radius:999px;font-weight:700;color:var(--mut)}
.seg button.on{background:var(--card);color:var(--tx);box-shadow:0 2px 8px rgba(0,0,0,.08)}
.fabrow{display:flex;gap:10px;padding:0 16px 8px;overflow-x:auto;scrollbar-width:none}
.fabrow::-webkit-scrollbar{display:none}
/* ---------- OVERLAYS ---------- */
#ovl{position:fixed;inset:0;z-index:90;display:none}
#ovl.on{display:block}
.ovlbg{position:absolute;inset:0;background:rgba(5,15,8,.55);animation:fade .2s}
@keyframes fade{from{opacity:0}}
.shb{position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:480px;background:var(--card);border-radius:26px 26px 0 0;padding:10px 20px calc(24px + env(safe-area-inset-bottom));animation:up .28s cubic-bezier(.2,.9,.3,1)}
@keyframes up{from{transform:translate(-50%,60%)}}
.grab{width:42px;height:5px;border-radius:99px;background:var(--line);margin:4px auto 14px}
.shb h3{font-family:Sora,sans-serif;font-size:19px;margin-bottom:14px}
.mdb{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:26px}
.mdc{background:var(--card);border-radius:22px;padding:24px;width:100%;max-width:360px;animation:popin .22s cubic-bezier(.2,.9,.3,1.2)}
@keyframes popin{from{transform:scale(.9);opacity:0}}
.mdc h3{font-family:Sora,sans-serif;font-size:20px;margin-bottom:8px}
#toast{position:fixed;bottom:calc(76px + env(safe-area-inset-bottom));left:50%;transform:translateX(-50%);z-index:120;display:flex;flex-direction:column;gap:8px;align-items:center;width:max-content;max-width:90vw}
.tst{background:#1b2a20;color:#fff;padding:11px 18px;border-radius:999px;font-size:13.5px;font-weight:600;box-shadow:0 8px 24px rgba(0,0,0,.3);animation:tst 2.6s forwards;max-width:88vw;text-align:center}
.tst.err{background:#7f1d1d}
@keyframes tst{0%{opacity:0;transform:translateY(10px)}8%,84%{opacity:1;transform:none}100%{opacity:0;transform:translateY(-6px)}}
/* ---------- CHAT ---------- */
.cwrap{display:flex;flex-direction:column;height:100dvh}
.cmsgs{flex:1;overflow-y:auto;padding:14px 14px 6px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:76%;padding:10px 14px;border-radius:19px;font-size:14.5px;line-height:1.4;word-break:break-word}
.msg.me{align-self:flex-end;background:var(--g2);color:#fff;border-bottom-right-radius:6px}
.msg.them{align-self:flex-start;background:var(--soft);border-bottom-left-radius:6px}
.msg .mt{display:block;font-size:10.5px;opacity:.65;margin-top:3px}
.typing{align-self:flex-start;background:var(--soft);border-radius:19px;border-bottom-left-radius:6px;padding:12px 16px;display:flex;gap:5px}
.typing i{width:7px;height:7px;border-radius:50%;background:var(--mut);animation:tp 1s infinite}
.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}
@keyframes tp{40%{transform:translateY(-4px)}}
.cinp{display:flex;gap:10px;padding:10px 14px calc(12px + env(safe-area-inset-bottom))}
.cinp .inp{flex:1;margin:0;height:46px}
.cinp button{width:46px;height:46px;border-radius:50%;background:var(--g2);color:#fff;display:flex;align-items:center;justify-content:center;flex:none}
.cmtrow{display:flex;gap:10px;padding:10px 0}
.cmtrow .av{width:32px;height:32px}
/* ---------- NOTIFS ---------- */
.nrow{display:flex;gap:12px;align-items:center;padding:13px 16px;border-bottom:1px solid var(--line);background:var(--card)}
.nrow.unread{background:#eef9f1}
[data-theme=dark] .nrow.unread{background:#12241a}
.nrow .nic{width:36px;height:36px;border-radius:50%;background:var(--soft);color:var(--g2);display:flex;align-items:center;justify-content:center;flex:none}
.nrow p{flex:1;font-size:14px;line-height:1.4}
.nrow .tm{font-size:11.5px;color:var(--mut);flex:none}
.minib{padding:8px 14px;border-radius:999px;background:var(--g2);color:#fff;font-weight:700;font-size:13px}
.minib.ghost{background:var(--soft);color:var(--tx)}
/* ---------- PROFILE ---------- */
.pfhead{display:flex;align-items:center;gap:18px;padding:18px 18px 8px}
.pfav{width:82px;height:82px;border-radius:50%;object-fit:cover;border:3px solid var(--g2)}
.pfstats{flex:1;display:flex;justify-content:space-around;text-align:center}
.pfstats b{display:block;font-family:Sora,sans-serif;font-size:18px}
.pfstats span{font-size:12.5px;color:var(--mut)}
.pfbio{padding:4px 18px 12px;font-size:14px;line-height:1.45}
.pfbtns{display:flex;gap:9px;padding:0 18px 14px}
.pfbtns .btn{padding:10px;font-size:14px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;padding:0 2px 80px}
.g3 .gi{aspect-ratio:1;position:relative;overflow:hidden}
.g3 img{width:100%;height:100%;object-fit:cover}
.g3 .reelb{position:absolute;top:7px;right:7px;color:#fff;filter:drop-shadow(0 1px 3px rgba(0,0,0,.6))}
/* ---------- REELS ---------- */
.reels{height:calc(100dvh - 104px);overflow-y:auto;scroll-snap-type:y mandatory;background:#000}
.reel{height:100%;scroll-snap-align:start;position:relative;display:flex;align-items:flex-end;color:#fff}
.reel>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:kb 18s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.14)}}
.reel .rinfo{position:relative;padding:0 16px 20px;width:72%;text-shadow:0 1px 6px rgba(0,0,0,.6)}
.reel .rail{position:relative;margin-left:auto;padding:0 12px 24px;display:flex;flex-direction:column;gap:16px;align-items:center}
.reel .rail button{color:#fff;display:flex;flex-direction:column;align-items:center;gap:3px;font-size:11.5px;font-weight:700}
/* ---------- GAMES ---------- */
.coinchip{display:flex;align-items:center;gap:7px;background:var(--soft);border:1.5px solid var(--line);border-radius:999px;padding:7px 14px;font-weight:800;color:var(--g2)}
.ludofeat{margin:6px 16px 14px;background:var(--gdeep);border-radius:20px;padding:20px;color:#fff;position:relative;overflow:hidden}
.ludofeat::after{content:"";position:absolute;right:-40px;top:-40px;width:170px;height:170px;border-radius:50%;background:rgba(255,255,255,.07)}
.ludofeat h3{font-family:Sora,sans-serif;font-size:21px}
.ludofeat p{opacity:.8;font-size:13px;margin:4px 0 14px}
.ludofeat .btn{background:#fff;color:var(--gdeep);width:auto;display:inline-block;padding:11px 26px}
.grow{display:flex;align-items:center;gap:13px;background:var(--card);border:1px solid var(--line);border-radius:18px;margin:0 16px 12px;padding:15px}
.grow .ric{width:46px;height:46px;border-radius:14px;background:var(--soft);color:var(--g2);display:flex;align-items:center;justify-content:center;flex:none}
.grow b{display:block;font-size:15px}
.grow span{font-size:12.5px;color:var(--mut)}
.grow .btn{margin-left:auto;width:auto;padding:9px 18px;font-size:13.5px}
.gstage{display:flex;flex-direction:column;align-items:center;padding:10px 20px 40px}
/* wheel */
.wheelwrap{position:relative;width:270px;height:270px;margin:16px 0}
.wheelwrap .ptr{position:absolute;top:-4px;left:50%;transform:translateX(-50%);color:var(--tx);z-index:2}
.wheelwrap .ptr svg{transform:rotate(90deg)}
/* dice */
.dice{width:86px;height:86px;border-radius:20px;background:var(--card);border:1.5px solid var(--line);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(0,0,0,.08)}
.dice.rolling{animation:shk .5s}
@keyframes shk{20%{transform:rotate(-14deg)}45%{transform:rotate(12deg)}70%{transform:rotate(-8deg)}}
/* memory */
.memg{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;width:100%;max-width:340px}
.mcard{aspect-ratio:1;border-radius:14px;position:relative;transform-style:preserve-3d;transition:transform .35s;cursor:pointer}
.mcard.flip{transform:rotateY(180deg)}
.mcard .fc{position:absolute;inset:0;border-radius:14px;backface-visibility:hidden;display:flex;align-items:center;justify-content:center}
.mcard .bk{background:var(--g2);color:#fff}
.mcard .fr{background:var(--card);border:1.5px solid var(--line);transform:rotateY(180deg);color:var(--g2)}
.mcard.done .fr{background:var(--soft);color:var(--g3)}
/* ---------- LUDO ---------- */
.lwrap{padding:8px 14px 30px}
.lboard{position:relative;width:100%;aspect-ratio:1;border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 8px 26px rgba(0,0,0,.1)}
.lc{position:absolute;width:6.667%;height:6.667%;border:1px solid #d8e2da;background:#fff}
.lsafe{background:#eef9f1}
.lh0{background:#fde3e4}.lh1{background:#def5e7}.lh2{background:#fbf0d8}.lh3{background:#dfe9fb}
.lyd{position:absolute;width:40%;height:40%;padding:9%}
.lydin{width:100%;height:100%;border:4px solid;border-radius:16px;background:#fff;position:relative}
.lslot{position:absolute;width:26%;height:26%;border-radius:50%;border:2px dashed #c8d5cb}
.lslot:nth-child(1){top:8%;left:8%}.lslot:nth-child(2){top:8%;right:8%}.lslot:nth-child(3){bottom:8%;left:8%}.lslot:nth-child(4){bottom:8%;right:8%}
.lctr{position:absolute;left:40%;top:40%;width:20%;height:20%;background:conic-gradient(#17b558 0 90deg,#df9a26 90deg 180deg,#3b82f6 180deg 270deg,#e5484d 270deg 360deg)}
.ltok{position:absolute;width:5.4%;height:5.4%;border-radius:50%;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.4);transform:translate(-50%,-50%);transition:left .13s linear,top .13s linear;z-index:3}
.ltok.move{animation:tkpulse .8s infinite;cursor:pointer;z-index:4}
@keyframes tkpulse{50%{box-shadow:0 0 0 7px rgba(23,181,88,.25)}}
.lhud{display:flex;align-items:center;gap:12px;padding:14px 4px}
.ldie{width:52px;height:52px;border-radius:12px;background:var(--card);border:1.5px solid var(--line);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(0,0,0,.08)}
.ldie.rolling{animation:shk .5s}
/* ---------- LIVE ---------- */
.livesurf{position:relative;background:#000;aspect-ratio:3/4;max-height:70dvh;width:100%;overflow:hidden}
.livesurf video,.livesurf canvas{width:100%;height:100%;object-fit:cover}
.livesurf.mirror video{transform:scaleX(-1)}
.livemeta{position:absolute;top:12px;left:12px;right:12px;display:flex;gap:8px;align-items:center}
.livebadge{background:var(--red);color:#fff;font-weight:800;font-size:11.5px;letter-spacing:1px;padding:5px 10px;border-radius:8px}
.vcbadge{background:rgba(0,0,0,.55);color:#fff;font-weight:700;font-size:12.5px;padding:5px 11px;border-radius:8px}
.lchat{position:absolute;bottom:0;left:0;right:0;padding:10px 12px 14px;display:flex;flex-direction:column;gap:5px;max-height:44%;overflow:hidden;justify-content:flex-end}
.lmsg{background:rgba(0,0,0,.5);color:#fff;border-radius:14px;padding:6px 12px;font-size:13px;width:max-content;max-width:85%;animation:up2 .25s}
@keyframes up2{from{transform:translateY(8px);opacity:0}}
.lmsg b{color:#7ef0a8}
.lheart{position:absolute;color:#ff5a76;animation:hh 1.6s ease-out forwards;pointer-events:none}
@keyframes hh{0%{opacity:1;transform:translateY(0) scale(.7)}100%{opacity:0;transform:translateY(-160px) scale(1.3)}}
/* ---------- WALLET ---------- */
.balcard{margin:8px 16px 16px;background:var(--gdeep);border-radius:22px;padding:24px;color:#fff;position:relative;overflow:hidden}
.balcard::after{content:"";position:absolute;right:-50px;bottom:-70px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,.06)}
.balcard .amt{font-family:Sora,sans-serif;font-weight:800;font-size:38px;letter-spacing:-1px}
.balrow{display:flex;gap:10px;margin-top:16px;position:relative;z-index:1}
.balrow .btn{flex:1;padding:12px;font-size:14px}
.tx{display:flex;align-items:center;gap:12px;padding:13px 16px;border-bottom:1px solid var(--line)}
.tx .tic{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none;background:var(--soft);color:var(--g2)}
.tx.neg .tic{color:var(--red)}
.tx b{font-size:14px;display:block}
.tx span{font-size:12px;color:var(--mut)}
.tx .amt{margin-left:auto;font-weight:800;font-family:Sora,sans-serif}
.tx .amt.pos{color:var(--g2)}.tx .amt.neg{color:var(--red)}
.stag2{font-size:11px;font-weight:800;padding:4px 10px;border-radius:99px;letter-spacing:.5px}
.stag2.pend{background:#fff3d6;color:#8a6410}.stag2.ok{background:#ddf5e6;color:#0a7c3d}.stag2.no{background:#fde3e4;color:#b3252b}
/* ---------- STORY VIEWER ---------- */
.strv{position:fixed;inset:0;z-index:100;background:#000;display:flex;align-items:center;justify-content:center}
.strv .smedia{max-width:480px;width:100%;height:100dvh;position:relative}
.strv .smedia img{width:100%;height:100%;object-fit:contain}
.sbars{position:absolute;top:10px;left:12px;right:12px;display:flex;gap:5px;z-index:2}
.sbars i{flex:1;height:3px;border-radius:99px;background:rgba(255,255,255,.3);overflow:hidden;position:relative}
.sbars i.done::after{content:"";position:absolute;inset:0;background:#fff}
.sbars i.cur::after{content:"";position:absolute;inset:0;background:#fff;animation:sbar 5s linear forwards}
@keyframes sbar{from{width:0}to{width:100%}}
.shead{position:absolute;top:26px;left:14px;right:14px;display:flex;align-items:center;gap:10px;color:#fff;z-index:2}
.shead img{width:34px;height:34px;border-radius:50%;border:1.5px solid rgba(255,255,255,.6)}
.stap{position:absolute;top:0;bottom:0;width:33%;z-index:1}
/* ---------- MISC ---------- */
.empty{text-align:center;padding:60px 30px;color:var(--mut)}
.empty .ric{width:70px;height:70px;border-radius:24px;background:var(--soft);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;color:var(--g2)}
.filterstrip{display:flex;gap:10px;overflow-x:auto;padding:12px 16px;scrollbar-width:none}
.filterstrip::-webkit-scrollbar{display:none}
.fth{flex:none;width:74px;text-align:center;font-size:12px;font-weight:700;color:var(--mut)}
.fth.on{color:var(--g2)}
.fth img,.fth .fph{width:74px;height:74px;border-radius:14px;object-fit:cover;border:2.5px solid transparent}
.fth.on img,.fth.on .fph{border-color:var(--g2)}
.fph{background:linear-gradient(140deg,#123822,#0a7c3d)}
.medprev{margin:8px 16px;border-radius:20px;overflow:hidden;background:#000;position:relative;aspect-ratio:4/3;max-height:44dvh}
.medprev img,.medprev video,.medprev canvas{width:100%;height:100%;object-fit:cover;display:block}
.medprev.mirror video{transform:scaleX(-1)}
textarea.inp2{width:100%;background:var(--soft);border:1.6px solid var(--line);border-radius:18px;padding:14px 16px;outline:0;resize:none;min-height:90px}
textarea.inp2:focus{border-color:var(--g2)}
select.pillsel{appearance:none;background:var(--soft);border:1.6px solid var(--line);border-radius:999px;height:50px;padding:0 17px;outline:0;width:100%;margin-bottom:12px}
.pagebody{padding:6px 22px 60px;line-height:1.7;font-size:14.5px}
.pagebody h3{font-family:Sora,sans-serif;margin:20px 0 6px;font-size:16px}
.pagebody p{color:var(--mut);margin-bottom:8px}
.faq{border-bottom:1px solid var(--line);padding:14px 2px}
.faq summary{font-weight:700;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center}
.faq summary::after{content:"+";font-family:Sora,sans-serif;color:var(--g2);font-size:18px}
.faq[open] summary::after{content:"–"}
.faq p{margin-top:8px}
.hint{font-size:12.5px;color:var(--mut);padding:0 18px 12px;line-height:1.5}
</style>
</head>
<body>
<div id="app"></div>
<div id="ovl"></div>
<div id="str"></div>
<div id="toast"></div>
<script>
/* ============================================================
   ZAR — single-file social + earning app prototype.
   DB = localStorage. Real-time between tabs = BroadcastChannel.
   ============================================================ */
'use strict';
const $=(s,el=document)=>el.querySelector(s), $$=(s,el=document)=>[...el.querySelectorAll(s)];
const app=$('#app');
const uid=(p='')=>p+Math.random().toString(36).slice(2,10);
const now=()=>Date.now();
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ago=t=>{const s=(now()-t)/1e3;if(s<60)return'now';if(s<3600)return(s/60|0)+'m';if(s<86400)return(s/3600|0)+'h';if(s<604800)return(s/86400|0)+'d';return new Date(t).toLocaleDateString()};
const wait=ms=>new Promise(r=>setTimeout(r,ms));
const hash=s=>{let h1=0xdeadbeef,h2=0x41c6ce57;const x=s+'|zar-salt';for(let i=0;i<x.length;i++){const c=x.charCodeAt(i);h1=Math.imul(h1^c,2654435761);h2=Math.imul(h2^c,1597334677)}h1=Math.imul(h1^(h1>>>16),2246822507)^Math.imul(h2^(h2>>>13),3266489909);h2=Math.imul(h2^(h2>>>16),2246822507)^Math.imul(h1^(h1>>>13),3266489909);return(h2>>>0).toString(16)+(h1>>>0).toString(16)};

/* action registry — declared early so every section can attach handlers */
const ACT={};

/* ---------- icons (inline SVG, stroke style) ---------- */
const IC={
home:'<path d="M3 10.6 12 3l9 7.6"/><path d="M5 9.5V21h5v-6h4v6h5V9.5"/>',
search:'<circle cx="11" cy="11" r="7"/><path d="m16.5 16.5 4.5 4.5"/>',
plus:'<path d="M12 5v14M5 12h14"/>',
plusSq:'<rect x="4" y="4" width="16" height="16" rx="4.5"/><path d="M12 8.5v7M8.5 12h7"/>',
heart:'<path class="f" d="M20.8 8.6a5 5 0 0 0-8.8-2.3A5 5 0 0 0 3.2 8.6C3.2 13 12 19.6 12 19.6s8.8-6.6 8.8-11z"/>',
comment:'<path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5c-1.5 0-3-.4-4.2-1L3 20l1.1-5A8.5 8.5 0 1 1 21 11.5z"/>',
share:'<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/>',
bookmark:'<path class="f" d="M6 3h12v18l-6-4.2L6 21z"/>',
bell:'<path d="M18 9a6 6 0 1 0-12 0c0 7-3 8-3 8h18s-3-1-3-8"/><path d="M10.3 21a2 2 0 0 0 3.4 0"/>',
film:'<rect x="3" y="3" width="18" height="18" rx="4.5"/><path d="M3 9h18M9 3.5 12 9M15.5 3.5 18.5 9"/>',
gamepad:'<rect x="2.5" y="7.5" width="19" height="11" rx="5.5"/><path d="M7 10.8v4M5 12.8h4"/><circle cx="16" cy="11.5" r=".9"/><circle cx="18.4" cy="14.2" r=".9"/>',
user:'<circle cx="12" cy="8" r="4"/><path d="M4 21c.9-4 4.2-6 8-6s7.1 2 8 6"/>',
users:'<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5 6.5-5s5.7 1.5 6.5 5"/><path d="M16 5.6a3.5 3.5 0 0 1 0 5.8M18.5 15.4c1.7.8 2.7 2.3 3 4.6"/>',
gear:'<circle cx="12" cy="12" r="3.2"/><path d="M12 2.6v2.8M12 18.6v2.8M2.6 12h2.8M18.6 12h2.8M5.3 5.3l2 2M16.7 16.7l2 2M18.7 5.3l-2 2M7.3 16.7l-2 2"/>',
chev:'<path d="m9 6 6 6-6 6"/>',
back:'<path d="m15 6-6 6 6 6"/>',
x:'<path d="M6 6l12 12M18 6 6 18"/>',
eye:'<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="2.8"/>',
eyeoff:'<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><path d="M4 4l16 16"/>',
mail:'<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3 7.5 9 6 9-6"/>',
lock:'<rect x="5" y="11" width="14" height="9" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
dots:'<circle cx="5" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/><circle cx="19" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
camera:'<path d="M4 8h3l2-3h6l2 3h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.5" r="3.5"/>',
video:'<rect x="2.5" y="6" width="13.5" height="12" rx="2.5"/><path d="m16 10.5 5.5-3.5v10l-5.5-3.5"/>',
live:'<circle cx="12" cy="12" r="2.4"/><path d="M7.8 7.8a6 6 0 0 0 0 8.4M16.2 7.8a6 6 0 0 1 0 8.4M4.9 4.9a10 10 0 0 0 0 14.2M19.1 4.9a10 10 0 0 1 0 14.2"/>',
coin:'<circle cx="12" cy="12" r="8.6"/><path d="M9 8.8h6L9 15.2h6"/>',
wallet:'<rect x="3" y="6" width="18" height="13" rx="3"/><path d="M3 10.2h18M15.5 14.6h.01" stroke-width="2.4"/>',
gift:'<rect x="3.5" y="8" width="17" height="4.5" rx="1.2"/><path d="M5 12.5V20h14v-7.5M12 8v12M12 8s-4.5.4-5.4-2C6 4.4 7.6 3.2 9 3.7c2 .7 3 4.3 3 4.3s1-3.6 3-4.3c1.4-.5 3 .7 2.4 2.3-.9 2.4-5.4 2-5.4 2z"/>',
moon:'<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/>',
globe:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a13.5 13.5 0 0 1 0 18M12 3a13.5 13.5 0 0 0 0 18"/>',
shield:'<path d="M12 3l7 2.8V12c0 4.6-3 7.9-7 9-4-1.1-7-4.4-7-9V5.8z"/>',
help:'<circle cx="12" cy="12" r="9"/><path d="M9.6 9.2a2.5 2.5 0 1 1 3.5 2.4c-.8.4-1.1 1-1.1 1.9"/><path d="M12 16.8h.01" stroke-width="2.6"/>',
flag:'<path d="M5 21V4h9l-1 3h7l-2 5 2 5h-9l-1-3H5"/>',
doc:'<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9.5 12h6M9.5 16h6"/>',
logout:'<path d="M9.5 4H5v16h4.5"/><path d="m14 8 4 4-4 4M8 12h10"/>',
trash:'<path d="M4 7h16M9.5 7V4h5v3M6 7l1 14h10l1-14M10 11v6M14 11v6"/>',
check:'<path d="m5 13 4 4L19 7"/>',
checkC:'<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.7 2.7L16.5 9.5"/>',
grid:'<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
copy:'<rect x="8.5" y="8.5" width="12" height="12" rx="2.5"/><path d="M5.5 15.5h-1a1 1 0 0 1-1-1v-10a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/>',
link:'<path d="M10 14a5 5 0 0 0 7.1 0l2.4-2.4a5 5 0 0 0-7.1-7.1L11 5.9"/><path d="M14 10a5 5 0 0 0-7.1 0l-2.4 2.4a5 5 0 0 0 7.1 7.1L13 18.1"/>',
dice:'<rect x="4" y="4" width="16" height="16" rx="3.5"/><circle cx="8.7" cy="8.7" r="1.15" fill="currentColor" stroke="none"/><circle cx="15.3" cy="15.3" r="1.15" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.15" fill="currentColor" stroke="none"/><circle cx="15.3" cy="8.7" r="1.15" fill="currentColor" stroke="none"/><circle cx="8.7" cy="15.3" r="1.15" fill="currentColor" stroke="none"/>',
spin:'<circle cx="12" cy="12" r="8.6"/><path d="M12 3.4v17.2M3.4 12h17.2M6 6l12 12M18 6 6 18"/>',
crown:'<path d="M4 18h16M4 18 3 9l5.5 4L12 6l3.5 7L21 9l-1 9z"/>',
ban:'<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
image:'<rect x="3" y="4" width="18" height="16" rx="2.5"/><circle cx="9" cy="10" r="2"/><path d="m3 17 5-5 4 4 3-3 6 5.5"/>',
play:'<path class="f" d="M8 5.4v13.2L19 12z" fill="currentColor"/>',
edit:'<path d="m4 20 1-4L16.5 4.5a2.12 2.12 0 0 1 3 3L8 19l-4 1z"/>',
key:'<circle cx="8" cy="15.5" r="4.2"/><path d="M11.2 12.3 20 3.5M16.2 5.5l3 3M13.6 8.1l3 3"/>',
info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.6h.01" stroke-width="2.2"/>',
zap:'<path d="M13 2 4.5 13.5H11l-1 8.5L18.5 10.5H12z"/>',
gem:'<path d="M6.5 3h11L21 9l-9 12L3 9z"/><path d="M3 9h18M12 21 8.2 9l3.8-6 3.8 6z"/>',
star:'<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5.2l3.4 2"/>',
phone:'<path d="M6 3h4l1.5 5L9 10a13 13 0 0 0 5 5l2-2.5 5 1.5v4a2 2 0 0 1-2 2A17 17 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
sliders:'<path d="M4 6h16M7 12h10M10 18h4"/>'
};
const I=(n,s=24,sw=1.8)=>`<svg class="ic" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round">${IC[n]||''}</svg>`;
const GICON=`<svg width="26" height="26" viewBox="0 0 24 24"><path fill="#EA4335" d="M12 5.04c1.62 0 3.06.56 4.2 1.66l3.12-3.12C17.46 1.8 14.96.75 12 .75 7.62.75 3.84 3.26 2.06 6.92l3.66 2.84C6.6 7.02 9.08 5.04 12 5.04z"/><path fill="#4285F4" d="M23.25 12.27c0-.93-.08-1.6-.26-2.3H12v4.36h6.44c-.13 1.08-.83 2.7-2.39 3.79l3.57 2.77c2.14-1.97 3.63-4.88 3.63-8.62z"/><path fill="#FBBC05" d="M5.73 14.24a6.9 6.9 0 0 1 0-4.48L2.06 6.92a11.26 11.26 0 0 0 0 10.16l3.67-2.84z"/><path fill="#34A853" d="M12 23.25c2.96 0 5.45-.98 7.28-2.65l-3.57-2.77c-.95.66-2.23 1.12-3.71 1.12-2.92 0-5.4-1.98-6.28-4.66l-3.66 2.84c1.78 3.66 5.56 6.12 9.94 6.12z"/></svg>`;
const FICON=`<svg width="26" height="26" viewBox="0 0 24 24"><path fill="#fff" d="M24 12a12 12 0 1 0-13.88 11.85v-8.38H7.08V12h3.04V9.36c0-3 1.79-4.67 4.53-4.67 1.31 0 2.68.23 2.68.23v2.95H15.8c-1.49 0-1.95.93-1.95 1.87V12h3.32l-.53 3.47h-2.79v8.38A12 12 0 0 0 24 12z"/></svg>`;
const AICON=`<svg width="24" height="24" viewBox="0 0 24 24" fill="#fff"><path d="M16.365 12.79c-.02-2.04 1.67-3.02 1.744-3.07-.95-1.39-2.43-1.58-2.955-1.6-1.26-.13-2.455.74-3.09.74-.64 0-1.63-.72-2.68-.7-1.38.02-2.65.8-3.36 2.03-1.43 2.48-.365 6.16 1.03 8.17.68.98 1.49 2.08 2.55 2.04 1.03-.04 1.41-.66 2.65-.66 1.24 0 1.58.66 2.66.64 1.1-.02 1.8-1 2.47-1.99.78-1.14 1.1-2.25 1.12-2.3-.025-.01-2.14-.82-2.16-3.26zM14.3 6.83c.565-.685.95-1.635.845-2.585-.815.033-1.8.545-2.385 1.227-.525.607-.985 1.577-.862 2.507.91.07 1.837-.462 2.402-1.149z"/></svg>`;
const BRAND=(s=56)=>`<svg width="${s}" height="${s}" viewBox="0 0 64 64" fill="none"><circle cx="32" cy="32" r="26" stroke="#fff" stroke-width="5"/><path d="M23 23h18L23 41h18" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

/* ---------- DB ---------- */
let DB=null, S={v:'splash',p:{tab:'home'},uid:localStorage.getItem('zarU')||null,authMode:'signup',rst:null,story:null,L:null};
let CLEAN=[]; const cleanup=()=>{CLEAN.forEach(f=>{try{f()}catch(e){}});CLEAN=[]};
const save=()=>{try{localStorage.setItem('zarDB',JSON.stringify(DB))}catch(e){toast('Storage full — media too large to keep','err')}};
const user=id=>DB.users.find(u=>u.id===id);
const me=()=>user(S.uid);
const post=id=>DB.posts.find(p=>p.id===id);
const follows=(a,b)=>DB.follows.some(f=>f.a===a&&f.b===b&&f.st==='ok');
const isBlockedBy=(a,b)=>user(a)?.blocked.includes(b);
const bus='BroadcastChannel' in window?new BroadcastChannel('zar-bus'):null;
if(bus)bus.onmessage=e=>{const m=e.data;if(!m)return;DB=JSON.parse(localStorage.getItem('zarDB'));S.uid=localStorage.getItem('zarU');
  if(m.t==='msg'){if(S.v==='chat'&&S.p.cid===m.cid)renderMsgs();else if(S.v==='app'||S.v==='chats')draw()}
  else if(m.t==='livechat'&&S.v==='watch'&&S.p.id===m.id)renderLiveChat(m.id);
  else if(m.t==='liveend'&&S.v==='watch')draw();
  else if(m.t==='live'||m.t==='post')draw()};

function avURI(name,c1,c2){const t=esc((name||'?').trim()[0]||'?').toUpperCase();
  const svg=`<svg xmlns='http://www.w3.org/2000/svg' width='96' height='96'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='${c1}'/><stop offset='1' stop-color='${c2}'/></linearGradient></defs><rect width='96' height='96' fill='url(#g)'/><text x='48' y='62' font-family='Sora,sans-serif' font-size='40' font-weight='700' fill='#fff' text-anchor='middle'>${t}</text></svg>`;
  return'data:image/svg+xml;utf8,'+encodeURIComponent(svg)}

function defSettings(){return{theme:'light',lang:'en',private:false,twofa:false,push:false,emailN:false,ntf:{like:true,comment:true,follow:true,msg:true,live:true}}}
function newUser(name,handle,email,pass,extra={}){
  const u={id:uid('u_'),name,handle,email:email.toLowerCase(),pass:hash(pass),bio:extra.bio||'New on Zar — here to share & earn',avatar:extra.avatar||avURI(name,'#17b558','#0a7c3d'),coins:0,admin:false,banned:false,blocked:[],pm:[],lastBonus:0,refBy:null,refEarn:0,phone:'',settings:defSettings(),created:now(),...extra};
  DB.users.push(u);return u}
function addCoins(id,amt,note){const u=user(id);if(!u)return;u.coins=Math.max(0,u.coins+amt);DB.tx.unshift({id:uid('t_'),uid:id,amt,note,t:now()});save()}
function notify(toId,type,text,data={}){if(toId===S.uid)return;const to=user(toId);if(!to||to.banned)return;if(to.settings.ntf[type]===false)return;DB.notifs.unshift({id:uid('n_'),to:toId,type,text,t:now(),read:false,data});save();if(bus)bus.postMessage({t:'sync'})}
function toast(msg,type){const d=document.createElement('div');d.className='tst'+(type==='err'?' err':'');d.textContent=msg;$('#toast').appendChild(d);setTimeout(()=>d.remove(),2700)}
function ovl(html){$('#ovl').innerHTML=`<div class="ovlbg"></div>${html}`;$('#ovl').classList.add('on')}
function sheet(html){ovl(`<div class="shb"><div class="grab"></div>${html}</div>`)}
function modal(html){ovl(`<div class="mdb"><div class="mdc">${html}</div></div>`)}
function closeOvl(){$('#ovl').classList.remove('on');$('#ovl').innerHTML=''}
 $('#ovl').addEventListener('click',e=>{if(e.target.classList.contains('ovlbg'))closeOvl()});
 $('#str').addEventListener('click',e=>{if(e.target.id==='strX'||e.target.closest('#strX'))closeStory()});
function applyTheme(){document.documentElement.dataset.theme=me()?.settings.theme||'light'}
function t(k){const lang=me()?.settings.lang||'en';
  const D={en:{home:'Home',search:'Search',profile:'Profile',games:'Games',reels:'Reels',newPost:'Create Post',goLive:'Go Live',playGames:'Play Games',playLudo:'Play Ludo',wallet:'Wallet',settings:'Settings',notifs:'Notifications',msgs:'Messages'},
  ur:{home:'ہوم',search:'تلاش',profile:'پروفائل',games:'کھیل',reels:'ریلز',newPost:'نیا پوسٹ',goLive:'لائیو جاؤ',playGames:'کھیل کھیلیں',playLudo:'لڈو کھیلیں',wallet:'والٹ',settings:'سیٹنگز',notifs:'اطلاعات',msgs:'پیغامات'}};
  return D[lang][k]||D.en[k]||k}

/* ---------- seed ---------- */
function seed(){
  DB={v:1,users:[],posts:[],stories:[],follows:[],notifs:[],chats:[],tx:[],withdrawals:[],reports:[],lives:[]};
  const mk=(name,handle,c1,c2,bio,extra={})=>newUser(name,handle,handle+'@zar.app','demo1234',{bio,avatar:avURI(name,c1,c2),...extra});
  const ay=mk('Ayesha Khan','ayesha','#17b558','#0a7c3d','Lahore — food, code & chai. Building small things.',{coins:1250});
  const bl=mk('Bilal Ahmed','bilal','#0e9147','#075c2d','Street photographer. Badshahi at golden hour > everything.',{coins:940});
  const za=mk('Zainab Malik','zainab','#2bb365','#128a44','Sketchbooks, parks & pencil dust.',{coins:610});
  const ha=mk('Hamza Sheikh','hamza','#31c95f','#0e9147','Cricket is not a hobby, it is a personality.',{coins:480});
  const fa=mk('Fatima Noor','fatima','#149c4d','#0a6b36','Desk setups & productivity nerd.',{coins:720});
  const us=mk('Usman Tariq','usman','#23bd62','#0d8443','Drones, kites, rooftops.',{coins:390});
  const ma=mk('Mariam S.','mariam','#1aa857','#0a7c3d','Hunza is home. Mountains are medicine.',{coins:860});
  newUser('Admin','zaradmin','admin@zar.app','admin123',{bio:'Zar platform administration',avatar:avURI('Z Admin','#0a7c3d','#073c1e'),admin:true});
  const H=(a,b)=>DB.follows.push({a:a.id,b:b.id,st:'ok',t:now()-86400e3});
  H(ay,bl);H(ay,za);H(ay,ma);H(ay,ha);H(bl,ay);H(za,ay);H(fa,ay);H(us,ay);H(ha,bl);H(ma,bl);H(fa,bl);
  const P=(u_,seedN,cap,likes,cms,extra={})=>{const p={id:uid('p_'),uid:u_.id,media:`https://picsum.photos/seed/${seedN}/900/1100.jpg`,cap,likes:likes.map(x=>x.id),savedBy:[],comments:cms.map(([cu,tx],i)=>({uid:cu.id,text:tx,t:now()-(i+2)*1800e3})),t:now()-(Math.random()*40+4)*3600e3,filter:'none',reel:false,...extra};DB.posts.push(p);return p};
  P(bl,'zar1','Golden hour at Badshahi Mosque. No filter needed. #lahore #photography',[ay,za,fa,ha],[[ay,'This shot is unreal!'],[za,'Golden hour magic, every time']]);
  P(ay,'zar2','Third attempt at biryani and I think I finally nailed it. Recipe in comments. #food #homemade',[bl,ma,za],[[bl,'Recipe please!'],[ma,'Tried it last night — 10/10']]);
  P(za,'zar3','Sketching session at the park. Two hours disappeared like minutes. #art',[ay,bl],[[ay,'The shading on the trees!']]);
  P(ha,'zar4','Match day. Stadium food is overpriced but the sixes are free. #cricket',[bl,us],[[us,'That last over though']]);
  P(ma,'zar5','Hunza mornings hit different. Worth every hour of the drive. #travel #pakistan',[ay,bl,fa,us],[[ay,'Adding this to my list'],[bl,'Light is incredible here']]);
  P(fa,'zar6','Desk setup refresh complete. Cable management is a form of self-care. #workspace',[ay,za],[[za,'What monitor arm is that?']]);
  P(us,'zar7','Kite festival from 120 meters up. The city looked like a painting. #basant #drone',[ha,ma],[[ha,'Top view!']]);
  P(bl,'zarr1','Street food crawl part 2 — the nihari place near the old gate. #reels #food',[ay,ha],[[ay,'My whole childhood in one video']],{reel:true,media:'https://picsum.photos/seed/zarr1/720/1280.jpg'});
  P(za,'zarr2','30 second speed sketch. Guess what it becomes. #art #reels',[ay],[[ay,'No way that is 30 seconds']],{reel:true,media:'https://picsum.photos/seed/zarr2/720/1280.jpg'});
  P(ma,'zarr3','Hunza in motion. Sound on. #travel #reels',[fa,us,ay],[],{reel:true,media:'https://picsum.photos/seed/zarr3/720/1280.jpg'});
  P(ha,'zarr4','Sixes only. Practice session highlights. #cricket #reels',[bl],[[bl,'That cover drive though']],{reel:true,media:'https://picsum.photos/seed/zarr4/720/1280.jpg'});
  DB.stories.push({id:uid('s_'),uid:bl.id,media:'https://picsum.photos/seed/zars1/720/1280.jpg',filter:'none',t:now()-2*3600e3,seenBy:[]},
                  {id:uid('s_'),uid:za.id,media:'https://picsum.photos/seed/zars2/720/1280.jpg',filter:'saturate(1.3)',t:now()-5*3600e3,seenBy:[]},
                  {id:uid('s_'),uid:ma.id,media:'https://picsum.photos/seed/zars3/720/1280.jpg',filter:'none',t:now()-60*60e3,seenBy:[]});
  DB.chats.push({id:uid('c_'),m:[ay.id,bl.id],msgs:[{from:bl.id,text:'Salam! Did you see the mosque shots I posted?',t:now()-5*3600e3,read:true},{from:ay.id,text:'Just liked them — the golden hour one is unreal',t:now()-4.8*3600e3,read:true}]},
                {id:uid('c_'),m:[ay.id,za.id],msgs:[{from:za.id,text:'Ludo tonight? Loser makes chai for a week',t:now()-26*3600e3,read:false}]});
  DB.lives.push({id:uid('l_'),uid:bl.id,title:'Old city food tour — live from Delhi Gate',t:now()-9*60e3,viewers:34,chat:[{n:'fatima',x:'The nihari looks amazing'},{n:'usman',x:'Salam from Multan!'}],active:true});
  DB.notifs.push({id:uid('n_'),to:ay.id,type:'follow',text:'fatima started following you',t:now()-3*3600e3,read:false,data:{uid:fa.id}},
                 {id:uid('n_'),to:ay.id,type:'like',text:'bilal liked your post',t:now()-4*3600e3,read:true,data:{}});
  DB.tx.push({id:uid('t_'),uid:ay.id,amt:200,note:'Welcome bonus',t:now()-6*86400e3},{id:uid('t_'),uid:ay.id,amt:150,note:'Ludo victory',t:now()-2*86400e3},{id:uid('t_'),uid:ay.id,amt:100,note:'Referral: hamza joined',t:now()-4*86400e3});
  save()}

function load(){try{DB=JSON.parse(localStorage.getItem('zarDB'))}catch(e){DB=null}
  if(!DB||DB.v!==1){seed();return}
  const cut=now()-86400e3;const n=DB.stories.length;DB.stories=DB.stories.filter(s=>s.t>cut);
  if(n!==DB.stories.length)save()}
setInterval(()=>{if(!DB)return;const cut=now()-86400e3;const n=DB.stories.length;DB.stories=DB.stories.filter(s=>s.t>cut);if(n!==DB.stories.length)save()},60e3);

/* ---------- router ---------- */
let HIST=[];
function go(v,p={}){HIST.push({v:S.v,p:S.p});S.v=v;S.p=p;draw()}
function back(){const h=HIST.pop()||{v:me()?'app':'splash',p:{tab:'home'}};S.v=h.v;S.p=h.p;draw()}
function tabx(tb){HIST=[];S.v='app';S.p={tab:tb,sub:null};draw()}
function draw(){cleanup();closeOvl();applyTheme();(R[S.v]||R.splash)();window.scrollTo(0,0)}
function login(id){S.uid=id;localStorage.setItem('zarU',id);save();HIST=[];S.v='app';S.p={tab:'home'};draw()}
function logout(){S.uid=null;localStorage.removeItem('zarU');S.v='splash';S.p={};draw()}

/* ---------- shared components ---------- */
function tbHTML(title,acts=''){return`<div class="tb"><button data-act="back">${I('back',24)}</button><span class="tbtitle">${title}</span><div class="tbacts">${acts||'<span style="width:40px"></span>'}</div></div>`}
function coinChip(n){return`<span class="coinchip">${I('coin',18,2.2)} ${n}</span>`}
function navHTML(active){const u=me();
  const b=(tb,ic)=>`<button data-act="tab" data-tb="${tb}" class="${active===tb?'on':''}">${I(ic,26)}</button>`;
  const pf=active==='profile'?`<img class="pav" src="${u.avatar}">`:I('user',26);
  /* Instagram layout: Home · Search · + · Reels · Profile — all at the bottom */
  return`<div class="nav">${b('home','home')}${b('search','search')}<button data-act="plus" class="plusbtn" aria-label="Create">${I('plusSq',26)}</button>${b('reels','film')}<button data-act="tab" data-tb="profile" class="${active==='profile'?'on':''}">${pf}</button></div>`}
function switchEl(k,on){return`<span class="sw ${on?'on':''}" data-act="tgl" data-k="${k}"><i></i></span>`}
function likesLine(p){const n=p.likes.length;if(!n)return'<span style="color:var(--mut);font-weight:500">Be the first to like this</span>';
  const first=p.likes.includes(S.uid)?'You':(user(p.likes[0])?.name||'Someone');
  return`Liked by ${esc(first)}${n>1?` and ${n-1} others`:''}`}
const fmtCap=s=>esc(s).replace(/#(\w+)/g,'<span class="htg">#$1</span>');
function postCard(p){
  const u=user(p.uid);if(!u)return'';const liked=p.likes.includes(S.uid),saved=(p.savedBy||[]).includes(S.uid);
  return`<div class="pcard" id="pc-${p.id}">
  <div class="phead"><img class="av" src="${u.avatar}" data-act="uprof" data-uid="${u.id}"><div style="flex:1;min-width:0"><div class="nm" data-act="uprof" data-uid="${u.id}">${esc(u.name)}</div><div class="sub mut">@${u.handle} · ${ago(p.t)}</div></div><button data-act="morep" data-pid="${p.id}" style="padding:8px">${I('dots',22)}</button></div>
  <div class="pmedia" data-act="dbl" data-pid="${p.id}"><img src="${p.media}" style="filter:${p.filter||'none'}" loading="lazy" alt=""><div class="bigh" id="bh-${p.id}">${I('heart',92)}</div></div>
  <div class="pacts">
    <button class="pa icbtn ${liked?'on':''}" id="hb-${p.id}" data-act="like" data-pid="${p.id}">${I('heart',26)}</button>
    <button class="pa" data-act="comments" data-pid="${p.id}">${I('comment',26)}</button>
    <button class="pa" data-act="sharep" data-pid="${p.id}">${I('share',25)}</button>
    <button class="pa save ${saved?'on':''}" data-act="savep" data-pid="${p.id}">${I('bookmark',25)}</button></div>
  <div class="plikes" id="lk-${p.id}">${likesLine(p)}</div>
  <div class="pcap"><b>${esc(u.name)}</b> ${fmtCap(p.cap)}</div>
  ${p.comments.length>2?`<div class="pviewall" id="va-${p.id}" data-act="comments" data-pid="${p.id}">View all ${p.comments.length} comments</div>`:''}
  <div class="pc2">${p.comments.slice(-2).map(c=>`<div><b>${esc(user(c.uid)?.name||'User')}</b> ${fmtCap(c.text)}</div>`).join('')}</div>
  <div class="ptime">${ago(p.t)} ago</div></div>`}
function refreshPost(pid){const p=post(pid);if(!p)return;const lk=$('#lk-'+pid);if(lk)lk.innerHTML=likesLine(p);
  const hb=$('#hb-'+pid);if(hb)hb.classList.toggle('on',p.likes.includes(S.uid));
  const va=$('#va-'+pid);if(va)va.textContent=p.comments.length>2?`View all ${p.comments.length} comments`:''}
function toggleLike(pid,forceOn){const p=post(pid);const i=p.likes.indexOf(S.uid);
  if(i>=0&&!forceOn){p.likes.splice(i,1)}else if(i<0){p.likes.push(S.uid);const a=user(p.uid);if(a)notify(a.id,'like',`${me().name} liked your post`,{pid});if(forceOn){const b=$('#bh-'+pid);if(b){b.classList.remove('go');void b.offsetWidth;b.classList.add('go')}}}
  save();refreshPost(pid)}

/* ============================================================ VIEWS */
const R={};

/* ---------- SPLASH ---------- */
R.splash=()=>{app.innerHTML=`<div class="mcol"><div class="splash">
  <div class="slogo">${BRAND(84)}</div><div class="sname">Zar</div><div class="stag">Share. Play. Earn.</div>
  <button class="getstart" data-act="getStarted">Get Started</button>
  <button class="haveacc" data-act="haveAcc">I already have an account</button></div></div>`};

/* ---------- AUTH ---------- */
R.auth=()=>{
  const m=S.authMode;const eyeBtn=`<button type="button" class="eye" data-act="eye">${I('eye',21)}</button>`;
  const signup=m==='signup',forgot=m==='forgot',reset=m==='reset';
  app.innerHTML=`<div class="mcol">
  <div class="authbg">${BRAND(58)}<div class="sname">Zar</div></div>
  <div class="sheet">
    <h2>${signup?'hello!':forgot||reset?'reset password':'welcome back!'}</h2>
    <p class="sub">${signup?'Create your account — share, play & earn':forgot?'We will verify you with a code':reset?'Enter the code and your new password':'Log in to continue earning'}</p>
    ${S.rst?`<div class="smallnote">No email server in this demo — your reset code is <b>${S.rst.code}</b>. (In production this is emailed.)</div>`:''}
    ${signup?`
    <div class="inp">${I('user',20)}<input id="a_name" placeholder="Full name" autocomplete="name"></div>
    <div class="inp">${I('user',20)}<input id="a_handle" placeholder="Username" autocomplete="username"></div>`:''}
    ${!reset?`<div class="inp">${I('mail',20)}<input id="a_email" type="email" placeholder="Email address" autocomplete="email"></div>`:''}
    ${reset?`<div class="inp">${I('shield',20)}<input id="a_code" placeholder="6-digit code" inputmode="numeric"></div>`:''}
    ${!forgot?`<div class="inp">${I('lock',20)}<input id="a_pass" type="password" placeholder="${reset?'New password':'Password'}">${eyeBtn}</div>`:''}
    ${signup?`<div class="inp">${I('gift',20)}<input id="a_ref" placeholder="Referral code (optional)"></div>`:''}
    <div class="aerr" id="autherr"></div>
    ${signup?`<div class="terms"><span class="cb" id="a_terms" data-act="termsCb">${I('check',14,3)}</span><span>I agree to the <button class="btnline" data-act="page" data-k="terms" style="padding:0">Terms of Service</button> and <button class="btnline" data-act="page" data-k="privacy" style="padding:0">Privacy Policy</button></span></div>`:''}
    <button class="btn" data-act="authSubmit">${signup?'Sign Up':forgot?'Send Reset Code':reset?'Update Password':'Log In'}</button>
    ${!forgot&&!reset?`
    <div class="divider">or</div>
    <div class="socials">
      <button class="soc gh" data-act="social" data-net="google" aria-label="Google">${GICON}</button>
      <button class="soc fb" data-act="social" data-net="facebook" aria-label="Facebook">${FICON}</button>
      <button class="soc ap" data-act="social" data-net="apple" aria-label="Apple">${AICON}</button></div>
    <div style="text-align:center;font-size:14px">${signup?`Already have an account? <button class="btnline" data-act="toLogin">Log in</button>`:`New to Zar? <button class="btnline" data-act="toSignup">Sign up</button>`}</div>
    ${!signup?`<div style="text-align:center;margin-top:12px"><button class="mut" style="font-weight:600;font-size:13.5px" data-act="forgotPw">Forgot password?</button></div>`:''}`:''}
    ${forgot||reset?`<div style="text-align:center;margin-top:16px"><button class="btnline" data-act="toLogin">Back to login</button></div>`:''}
    <button class="demolink" data-act="demo">Explore with a demo account →</button>
  </div></div>`;
  const p=$('#a_pass');if(p)p.addEventListener('input',()=>{if($('#a_pass').type==='text'&&p.value==='')ACT.eye()})};

/* ---------- APP SHELL + TABS ---------- */
R.app=()=>{
  const tab=S.p.tab||'home';let inner='';
  if(tab==='home')inner=vHome();
  else if(tab==='search')inner=vSearch();
  else if(tab==='reels')inner=vReels();
  else inner=vProfile(me());
  app.innerHTML=inner+navHTML(tab)};

function vHome(){
  const u=me();const followIds=DB.follows.filter(f=>f.a===S.uid&&f.st==='ok').map(f=>f.b);
  const lives=DB.lives.filter(l=>l.active&&l.uid!==S.uid&&!u.blocked.includes(l.uid));
  const stUsers=[...new Set(DB.stories.filter(s=>!u.blocked.includes(s.uid)).map(s=>s.uid))].filter(id=>user(id)&&!user(id).banned);
  stUsers.sort((a,b)=>{const ax=a===S.uid,bx=b===S.uid;if(ax!==bx)return ax?-1:1;return Math.max(...DB.stories.filter(s=>s.uid===b).map(s=>s.t))-Math.max(...DB.stories.filter(s=>s.uid===a).map(s=>s.t))});
  const unseen=id=>DB.stories.some(s=>s.uid===id&&!s.seenBy.includes(S.uid));
  const nUn=DB.notifs.some(n=>n.to===S.uid&&!n.read);
  const cUn=DB.chats.some(c=>c.m.includes(S.uid)&&c.msgs.some(m=>m.from!==S.uid&&!m.read));
  /* Instagram top
