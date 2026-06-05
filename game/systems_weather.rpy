# ===================================================================
# systems_weather.rpy
# Environment FX / Weather Layer (Reserved)
# ===================================================================
# 归属：Scene Presentation Layer → Environment FX / Weather Layer
# 状态：Reserved (2026-06-04 v3.0d)
#
# 当前作用：仅占接口，不实现任何具体天气动画。
# state 变量可读可写，但不会被任何渲染层消费。
# weather_layer screen 当前为空实现。
#
# 未来升级路径：
# 当天气需要影响剧情 / 数值 / 事件 / 存档时，
# 走 Framework Audit 升级为一级 Weather System。
# 届时将接 Audio System / Save System / Camera System / Video System。
#
# 禁止本轮实现：
#   - 雨/雪/雾/雷动画
#   - 配套音效
#   - 存档持久化
#   - 镜头闪光 / 色调蒙版
# ===================================================================

# ----- 状态变量 -----
# weather_type: "none" / "rain" / "snow" / "fog" / "thunder" / "wind"
default weather_type = "none"
# weather_intensity: 0~100
default weather_intensity = 0
# weather_wind: -100~100  (-=左，+=右)
default weather_wind = 0

# ----- 接口（Reserved，空实现）-----
init -1 python:
    def set_weather(weather_type, intensity=50, wind=0, transition=1.0):
        """Reserved: 切换天气。当前仅更新 state 变量，不触发动画。
        Args:
            weather_type: "none" / "rain" / "snow" / "fog" / "thunder" / "wind"
            intensity: 0~100
            wind: -100~100
            transition: 切换渐变时间（秒），当前未使用，留接口
        """
        store.weather_type = weather_type
        store.weather_intensity = intensity
        store.weather_wind = wind

    def stop_weather(transition=1.0):
        """Reserved: 关闭天气。当前仅重置 state 变量。"""
        store.weather_type = "none"
        store.weather_intensity = 0
        store.weather_wind = 0

    def get_weather_state():
        """Reserved: 返回当前天气状态 dict。"""
        return {
            "type": store.weather_type,
            "intensity": store.weather_intensity,
            "wind": store.weather_wind,
        }

# ----- 渲染层（Reserved，空实现）-----
# 由 explore_scene_test 等 screen 通过 `use weather_layer` 嵌入
# 当前不画任何东西；具体天气实现时在这里加 add Particle / add Solid / add Movie 等
screen weather_layer():
    # Reserved: 当前空实现
    # TODO（Framework Audit 升级 Weather System 后实现）:
    #   if weather_type == "rain":
    #       add ParticleSystem(...rain config...)
    #   elif weather_type == "snow":
    #       add ParticleSystem(...snow config...)
    #   elif weather_type == "fog":
    #       add "images/weather/fog_overlay.png" at fog_drift
    #   elif weather_type == "thunder":
    #       # 触发瞬时闪光走 Camera System，非 screen 层
    #       pass
    pass
