from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/crawl')
def crawl():
    # Setup chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run in background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://spot.wooribank.com/pot/Dream?withyou=POLON0055&cc=c010528:c010531;c012425:c012399&PLM_PDCD=P020006646&PRD_CD=P020006646&HOST_PRD_CD=2031168000000"
    
    try:
        driver.get(url)
        
        # Wait for the title to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
        
        page_title = driver.title
        
        return jsonify({{"title": page_title}})

    except Exception as e:
        return jsonify({{"error": str(e)}}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')