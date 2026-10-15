import flet as ft
import flet_webview as fwv

TARGET_URL = "https://yiban.gxnu.edu.cn/yzdx/dean/course"

def main(page: ft.Page):
    page.padding = 0
    page.spacing = 0

    async def JS_Injector(e):
        JS_Code = r"""
        (() => {
            document.documentElement.style.overscrollBehavior = "none";
            document.body.style.overscrollBehavior = "none";
            if (window._ListenerCleanup) {
                window._ListenerCleanup();
            }
            const IsDarkTheme = window.matchMedia(
                "(prefers-color-scheme: dark)"
            );
            function applyTheme() {
                const dark = IsDarkTheme.matches;
                const app = document.querySelector("#app");
                if (app) {
                    app.style.setProperty(
                    "background-color",
                    dark ? "#121212" : "#f8fafc",
                    "important"
                    );

                    app.style.setProperty(
                    "color",
                    dark ? "#e0e0e0" : "#111827",
                    "important"
                    );
                }
                const popup = document.querySelector(".van-popup");
                if (popup) {
                    popup.style.setProperty(
                    "background-color",
                    dark ? "#121212" : "#ffffff",
                    "important"
                    );
                    popup.querySelectorAll("*").forEach(child => {
                        child.style.setProperty(
                        "color",
                        dark ? "#e0e0e0" : "#111827",
                        "important"
                    );
                    });
                }
                const skeleton = document.querySelector(".van-skeleton-paragraph");
                if (skeleton) {
                    skeleton.style.setProperty(
                    "background-color",
                    dark ? "#333333" : "#eeeeee",
                    "important"
                    );
                }
                const cellGroup = document.querySelector(".van-cell-group");
                if (cellGroup) {
                    cellGroup.style.setProperty(
                    "background-color",
                    dark ? "#121212" : "#ffffff",
                    "important"
                    );
                    const vanCells = cellGroup.querySelectorAll(".van-cell");
                    vanCells.forEach(element => {
                        element.style.setProperty(
                            "background-color",
                            dark ? "#121212" : "#ffffff",
                            "important"
                        );
                        element.style.setProperty(
                        "color",
                        dark ? "#e0e0e0" : "#111827",
                        "important"
                        );
                    });
                }
                const backbutton = document.querySelector(".van-button--default");
                if(backbutton){
                    backbutton.style.setProperty(
                    "background-color",
                    dark ? "#121212" : "#ffffff",
                    "important"
                    );
                    backbutton.style.setProperty(
                    "color",
                    dark ? "#e0e0e0" : "#111827",
                    "important"
                    );
                }
                const van_action_sheet__content = document.querySelector(".van-action-sheet__content");
                if (van_action_sheet__content) {
                    const item = van_action_sheet__content.querySelectorAll(".van-action-sheet__item");
                    item.forEach(element => {
                        element.style.setProperty(
                            "background-color",
                            dark ? "#121212" : "#ffffff",
                            "important"
                        );
                        element.style.setProperty(
                        "color",
                        dark ? "#e0e0e0" : "#111827",
                        "important"
                        );
                        element.querySelectorAll("*").forEach(child => {
                            child.style.setProperty(
                                "color",
                                dark ? "#e0e0e0" : "#111827",
                                "important"
                            );
                        });
                    });
                }
                const cancelbutton = document.querySelector(".van-action-sheet__cancel");
                if(cancelbutton){
                    cancelbutton.style.setProperty(
                    "background-color",
                    dark ? "#121212" : "#ffffff",
                    "important"
                    );
                    cancelbutton.style.setProperty(
                    "color",
                    dark ? "#e0e0e0" : "#111827",
                    "important"
                    );
                }
                const sheet__gap = document.querySelector(".van-action-sheet__gap");
                if(sheet__gap){
                    sheet__gap.style.setProperty(
                    "background-color",
                    dark ? "#121212" : "#ffffff",
                    "important"
                    );
                }              
            }
            const Lessons = {
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
            const selector = ".flex.items-center.justify-center.min-h-10";
            function replaceLessons() {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {const text = element.textContent.trim();if (Object.prototype.hasOwnProperty.call(Lessons, text)) { element.innerHTML = Lessons[text]; }});
            }
            function updatePage() {
                applyTheme();
                const result = replaceLessons();
            }
            updatePage();
            IsDarkTheme.addEventListener("change", applyTheme);
            let updateScheduled = false;
            const observer = new MutationObserver(() => {
                if (updateScheduled) return;
                updateScheduled = true;
                requestAnimationFrame(() => {
                    updateScheduled = false;
                    updatePage();
                });
            });
            observer.observe(document.documentElement, {
                childList: true,
                subtree: true
            });
            window._ListenerCleanup = () => {
                IsDarkTheme.removeEventListener("change", applyTheme);
                observer.disconnect();
            };
        })();
        """
        await e.control.run_javascript(JS_Code)

    def create_webview():
        return fwv.WebView(
            url=TARGET_URL,
            expand=True,
            on_page_ended=JS_Injector,
        )

    webview_container = ft.Column(
        expand=True,
        spacing=0,
        controls=[create_webview()],
    )

    page.add(
        ft.SafeArea(
            content=webview_container,
            expand=True,
        )
    )

    last_state = {"value": None}

    async def reload(e):
        if e.state == ft.AppLifecycleState.RESUME:
            wv = webview_container.controls[0]

            try:
                url = await wv.get_current_url()

                if url is None:
                    webview_container.controls.clear()
                    webview_container.controls.append(create_webview())
                    page.update()

            except Exception as ex:
                webview_container.controls.clear()
                webview_container.controls.append(create_webview())
                page.update()

    page.on_app_lifecycle_state_change = reload

ft.run(main)
