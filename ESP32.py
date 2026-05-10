from machine import Pin,I2C
from time import sleep
import network
import ujson
import urequests
import sh1106

green = Pin(2, Pin.OUT)
yellow = Pin(4, Pin.OUT)
red = Pin(5, Pin.OUT)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = sh1106.SH1106_I2C(128, 64, i2c)
oled.fill(0)
oled.text("HELLO", 0, 0)

button = Pin(14, Pin.IN, Pin.PULL_UP)

SSID = "Wifi Username retracted"
PASSWORD = "Wifi Password Retracted"

GITHUB_OWNER = "Anubhav9"
GITHUB_REPO_NAME = "Make-CI-green-again"
GITHUB_BRANCH = "main"
GITHUB_WORKFLOW_NAME = "ci.yml"
GITHUB_TOKEN = "Token Retracted"

GITHUB_BASE_URL = "https://api.github.com/repos/{}/{}".format(
    GITHUB_OWNER,
    GITHUB_REPO_NAME,
)

HEADERS = {
    "Authorization": "Bearer " + GITHUB_TOKEN,
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "esp32-ci-monitor",
}



def connect_with_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")

    while not wifi.isconnected():
        print("Still connecting...")
        sleep(1)

    print("WiFi Connected!")
    print("IP Address:", wifi.ifconfig()[0])
    return True


def trigger_github_action():
    url = "{}/actions/workflows/{}/dispatches".format(
        GITHUB_BASE_URL,
        GITHUB_WORKFLOW_NAME,
    )

    payload = {
        "ref": GITHUB_BRANCH,
        "return_run_details": True,
    }

    print("Triggering:", url)

    response = urequests.post(url, headers=HEADERS, data=ujson.dumps(payload))
    status_code = response.status_code

    if status_code != 200:
        print("Trigger failed:", status_code)
        print(response.text)
        response.close()
        return None

    data = response.json()
    response.close()

    print("Run details:", data)

    # Depending on GitHub response shape, prefer URL if present.
    return data.get("id") or data.get("run_id") or data.get("workflow_run_id")


def get_current_status(run_id):
    url = "{}/actions/runs/{}".format(GITHUB_BASE_URL, run_id)

    response = urequests.get(url, headers=HEADERS)
    body = response.json()
    response.close()

    status = body.get("status")
    conclusion = body.get("conclusion")

    return status, conclusion


def poll_until_done(run_id):
    for i in range(10):
        status, conclusion = get_current_status(run_id)

        print("Status:", status, "Conclusion:", conclusion)

        if status == "completed":
            yellow.off()

            if conclusion == "success":
                green.on()
                red.off()
                return "success"

            red.on()
            green.off()
            return "failure"

        yellow.on()
        sleep(30)

    return "timeout"


def main():
    result_wifi = connect_with_wifi()

    if result_wifi:
        while True:
            last_button_state=1
            current_state=button.value()
            if last_button_state==1 and current_state==0:
                print("Button pressed, triggering GitHub Actions workflow")

                green.off()
                red.off()
                yellow.on()

                run_id = trigger_github_action()

                if run_id is None:
                    yellow.off()
                    red.on()
                    continue

                final_status = poll_until_done(run_id)
                print("Final status:", final_status)

                sleep(2)
            else:
                print("Button is not pressed, it should not trigger the API call")
                sleep(0.2)


main()
