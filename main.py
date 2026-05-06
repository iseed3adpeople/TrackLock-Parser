from playwright.async_api import async_playwright
import pandas as pd
import asyncio

async def parse():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            await page.goto("https://tracklock.gg/heroes-tier-list/7d/all/normal")

            rows = await page.locator("table tr").all()

            if not rows:
                raise ValueError("Таблица не найдена или пустая")

            data = []
            for row in rows:
                cells = await row.locator("td, th").all_text_contents()
                data.append(cells)

            if len(data) < 2:
                raise ValueError("Недостаточно данных в таблице")

            df = pd.DataFrame(data[1:], columns=data[0])
            pd.set_option("display.max_columns", None)
            pd.set_option("display.width", 1000)

            df.to_json("data.json", orient="records", force_ascii=False, indent=4)
            df.to_csv("data.csv", index=False)
            df.to_excel("data.xlsx", index=False)

            print("Данные успешно сохранены")

        except ValueError as e:
            print(f"Ошибка данных: {e}")

        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

        finally:
            await browser.close()
            print("Браузер закрыт")

if __name__ == "__main__":
    asyncio.run(parse())