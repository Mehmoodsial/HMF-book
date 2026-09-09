<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Style Menu Bar</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #fafafa;
            padding-bottom: 60px; /* Menu bar ke liye space */
        }

        .content {
            padding: 20px;
            text-align: center;
        }

        /* ===== BOTTOM MENU BAR (Instagram Style) ===== */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 55px;
            background: #ffffff;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid #dbdbdb;
            z-index: 1000;
        }

        .nav-item {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 20%;
            height: 100%;
            color: #262626;
            text-decoration: none;
            transition: transform 0.15s ease;
        }

        .nav-item:active {
            transform: scale(0.85);
        }

        .nav-item svg {
            width: 26px;
            height: 26px;
            stroke: #262626;
            fill: none;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        /* Active tab ka color */
        .nav-item.active svg {
            stroke: #0095f6;
        }
    </style>
</head>
<body>

    <!-- Aapka Content -->
    <div class="content">
        <h1>Welcome 👋</h1>
        <p>Yahan aapka page content hoga</p>
    </div>

    <!-- ===== BOTTOM MENU BAR ===== -->
    <nav class="bottom-nav">
        
        <!-- Home -->
        <a href="#" class="nav-item active">
            <svg viewBox="0 0 24 24">
                <path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1v-9.5z"/>
            </svg>
        </a>

        <!-- Search -->
        <a href="#" class="nav-item">
            <svg viewBox="0 0 24 24">
                <circle cx="11" cy="11" r="7"/>
                <line x1="16.5" y1="16.5" x2="21" y2="21"/>
            </svg>
        </a>

        <!-- Add / Plus -->
        <a href="#" class="nav-item">
            <svg viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="5"/>
                <line x1="12" y1="8" x2="12" y2="16"/>
                <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
        </a>

        <!-- Reels -->
        <a href="#" class="nav-item">
            <svg viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="5"/>
                <line x1="3" y1="8.5" x2="21" y2="8.5"/>
                <line x1="9" y1="3" x2="11" y2="8.5"/>
                <line x1="15" y1="3" x2="17" y2="8.5"/>
                <path d="M10 12.5l4.5 2.5-4.5 2.5v-5z"/>
            </svg>
        </a>

        <!-- Profile -->
        <a href="#" class="nav-item">
            <svg viewBox="0 0 24 24">
                <circle cx="12" cy="8" r="4"/>
                <path d="M4 21c0-4 3.5-6.5 8-6.5s8 2.5 8 6.5"/>
            </svg>
        </a>

    </nav>

    <!-- Tab switch karne ka JavaScript -->
    <script>
        const items = document.querySelectorAll('.nav-item');
        items.forEach(item => {
            item.addEventListener('click', function(e) {
                e.preventDefault();
                items.forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            });
        });
    </script>

</body>
</html>
