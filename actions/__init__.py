from .send_email.action import send_email
from .wait.action import wait
from .end.action import end

repository = {
    "send_email": send_email,
    "wait": wait,
    "end": end
}