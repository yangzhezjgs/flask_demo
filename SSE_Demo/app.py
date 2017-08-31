import datetime
import flask
import redis


app = flask.Flask(__name__)
app.secret_key = 'asdf'
red = redis.StrictRedis(host='localhost', port=6379, db=6)


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('time')
    for message in pubsub.listen():
        print (message)
        yield 'data: %s\n\n' % message['data']

@app.route('/post', methods=['POST'])
def post():
    now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish('time', u'%s' % (now.isoformat()))
    return flask.Response(status=204)


@app.route('/stream')
def stream():
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


@app.route('/')
def home():
    return u"""
        <!doctype html>
        <title>chat</title>
        <script src="http://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        </p><button id="time">Click for time!</button>
        <pre id="out"></pre>
        <script>
            function sse() {
                var source = new EventSource('/stream');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    out.innerHTML = 'now-tiem:'+ e.data + '\\n' + out.innerHTML;
                };
            }
            $('#time').click(function(){
                    $.post('/post');
                }
            );
            sse();
        </script>
    """ 


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
