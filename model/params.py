class params(object):
    
    def __init__(self):
        self.LW = 1e-5
        self.LC = 1e-5
        self.eta = 0.05

    def __str__(self):
        t = "LW", self.LW, ", LC", self.LC, ", eta", self.eta
        t = map(str, t)
        return ' '.join(t)
rmpc = 1
if __name__ == '__main__' :
    params = params()
    print('type',type(params))
    print('params',params)
    params.rmpc = rmpc
    print('type',type(params.rmpc))
    print('params.rmpc', params.rmpc)

    
    
