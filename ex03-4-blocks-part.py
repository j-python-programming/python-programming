    ball.vy = -ball.vy    # ボールの移動方向が変わる
    # の下に、以下の2行を追加する。
    # ボールの位置によって、反射角度を変える　(191行目付近)
    ball.vx = int(6 * (ball.x + ball.d/2 - pad.x) / pad.w) -3
