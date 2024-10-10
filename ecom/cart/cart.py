class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # get the current session key if existed
        cart = self.session.get('session_key')

        # if the user is new, create a session_key
        if 'session_key' not in cart:
            cart = self.session['session_key'] = {} 