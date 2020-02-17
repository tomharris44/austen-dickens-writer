from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests, time, math


def index(request):

    resp = requests.get("https://glacial-inlet-71849.herokuapp.com/get_latest")

    resp_json = resp.json()

    body = ''

    timer = """
        <p id="timer"></p>
        <script>

        // Get today's date and time
        var now = new Date();

        // Set the date we're counting down to
        var countDownDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours() + 1, 0, 0, 0).getTime();

        // Update the count down every 1 second
        var x = setInterval(function() {

            // Get today's date and time
            var now_date = new Date();
            var now = now_date.getTime();


            var countDownDate = new Date(now_date.getFullYear(), now_date.getMonth(), now_date.getDate(), now_date.getHours() + 1, 0, 0, 0).getTime();

            // Find the distance between now and the count down date
            var distance = countDownDate - now;

            // Time calculations for days, hours, minutes and seconds
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Display the result in the element with id="timer"
            document.getElementById("timer").innerHTML = "Time till next release: " + minutes + "m " + seconds + "s ";

            // If the count down is finished, write some text
            if (distance < 0) {
                clearInterval(x);
                document.getElementById("timer").innerHTML = "EXPIRED";
            }
        }, 1000);
        </script>
        <br/>
    """

    body = timer

    start = time.strptime("17 Feb 20 1:00:00", "%d %b %y %H:%M:%S")

    start = time.mktime(start)

    now = time.time()

    diff = now - start

    diff = math.floor(diff / (60 * 60))

    if diff > len(resp_json):
        diff = len(resp_json)

    # template = loader.get_template('writer/index.html')

    for i in range(0,diff):
        resp_json[i][1] = resp_json[i][1].replace('\n', '<br/>')
        resp_json[i][1] = resp_json[i][1].replace('"', "'")
        body = body + f'<div id=i><p><b>{resp_json[i][2]}</b>\n\n</p>'
        body = body + f'<p>{resp_json[i][1]}\n\n</p></div>'


    # context = {
    #     'latest': resp_json,
    # }

    return HttpResponse(body)
    # return HttpResponse(template.render(context, request))