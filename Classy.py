import flet as ft
import flet_webview as fwv


def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0

    async def on_page_ended(e):
        js_code = r"""
        (() => {
            // 清理上一次注入的监听器
            if (window.__kebiaoCleanup) {
                window.__kebiaoCleanup();
            }

            const media = window.matchMedia(
                "(prefers-color-scheme: dark)"
            );

            const lessons = {
                "1": "第1节<br>8:20<br>开始",
                "2": "第2节<br>9:40<br>结束",
                "3": "第3节<br>9:50-10:30",
                "4": "第4节<br>10:40<br>开始",
                "5": "第5节<br>12:00<br>结束",
                "6": "第6节<br>14:10-14:50",
                "7": "第7节<br>15:00-15:40",
                "8": "第8节<br>15:50-16:30",
                "9": "第9节<br>16:40-17:20",
                "10": "第10节<br>19:10-19:50",
                "11": "第11节<br>20:00-20:40",
                "12": "第12节<br>20:50-21:30"
            };

            const selector =
                ".flex.items-center.justify-center.min-h-10";

            function applyTheme() {
                const app = document.querySelector("#app");

                // 同时设置网页主题标记
                document.documentElement.dataset.theme =
                    media.matches ? "dark" : "light";

                document.documentElement.style.colorScheme =
                    media.matches ? "dark" : "light";

                if (!app) return;

                app.style.setProperty(
                    "background-color",
                    media.matches ? "#121212" : "#f8fafc",
                    "important"
                );

                app.style.setProperty(
                    "color",
                    media.matches ? "#e0e0e0" : "#111827",
                    "important"
                );
            }

            function replaceLessons() {
                const elements =
                    document.querySelectorAll(selector);

                let changed = 0;

                elements.forEach(element => {
                    const text = element.textContent.trim();

                    if (
                        Object.prototype.hasOwnProperty.call(
                            lessons, text
                        )
                    ) {
                        // 避免重复写入相同内容
                        if (
                            element.dataset.kebiaoDone !== text
                        ) {
                            element.innerHTML = lessons[text];
                            element.dataset.kebiaoDone = text;
                            changed++;
                        }
                    }
                });

                return {
                    found: elements.length,
                    changed: changed
                };
            }

            function updatePage() {
                applyTheme();

                const result = replaceLessons();

                console.log(
                    "[课表] 找到元素:",
                    result.found,
                    "本次替换:",
                    result.changed
                );
            }

            // 首次执行
            updatePage();

            // 监听系统主题切换
            media.addEventListener("change", applyTheme);

            // 处理 React 等框架稍后渲染课表的情况
            let updateScheduled = false;

            const observer = new MutationObserver(() => {
                if (updateScheduled) return;

                updateScheduled = true;

                // 合并短时间内的多次 DOM 变化
                requestAnimationFrame(() => {
                    updateScheduled = false;
                    updatePage();
                });
            });

            observer.observe(document.documentElement, {
                childList: true,
                subtree: true
            });

            window.__kebiaoCleanup = () => {
                media.removeEventListener(
                    "change", applyTheme
                );
                observer.disconnect();
            };

            console.log("[课表] JavaScript 注入成功");
        })();
        """

        try:
            await webview.run_javascript(js_code)
            print("已向 WebView 注入课表脚本")
        except Exception as ex:
            print("JavaScript 注入失败:", ex)

    webview = fwv.WebView(
        url="https://yiban.gxnu.edu.cn/yzdx/dean/course",
        expand=True,
        on_page_ended=on_page_ended,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    webview,
                ],
            ),
            expand=True,
        )
    )

    #暗黑模式整体应用的颜色切换，同事要观察用户的状态切换（说白了防手贱，一般用不到但还是考虑的多点比较好）（嘻嘻）
    #先试试，有问题再改
    page.bgcolor = "#121212" if is_dark else "#f8fafc"
    def on_brightness_change(e):
        is_dark_now = page.platform_brightness == ft.PlatformBrightness.DARK
        page.bgcolor = "#121212" if is_dark_now else "#f8fafc"
        # 如果需要，也可以在这里重新向 WebView 注入 JS
        # await webview.run_javascript(...)
        page.update()
    page.on_platform_brightness_change = on_brightness_change


ft.run(main)
