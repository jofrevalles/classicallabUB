
import numpy as np
import matplotlib.pyplot as plt
from particle import *
from potentials import *

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty,ListProperty,NumericProperty
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle,Color,Ellipse
from kivy.clock import Clock

L = 200


T = 30
dt = 0.1


class main(BoxLayout):
    
    
    param0 = NumericProperty()
    param1 = NumericProperty()
    param2 = NumericProperty()
    param3 = NumericProperty()
    
    mass = NumericProperty()
    charge = 1.
    x0 = NumericProperty()
    y0 = NumericProperty()
    vx0 = NumericProperty()
    vy0 = NumericProperty()
    
    
    potentials = ListProperty()
    particlestrings = ListProperty()
    particles = []
    init_conds = []
    
    plot_texture = ObjectProperty()
    
    
    def __init__(self, **kwargs):
        super(main, self).__init__(**kwargs)
        self.pot = Phi()
        self.set_texture()
        self.time = 0.
        self.T = 30
        
    def set_texture(self):
        L = 200
        dx = 1
        self.nx = int(L/dx)
        self.im = np.zeros((self.nx,self.nx),dtype=np.uint8)
        self.plot_texture = Texture.create(size=self.im.shape,colorfmt='luminance',bufferfmt='uint')
        
    def background(self):
        xx,yy, = np.meshgrid(np.linspace(-L/2.,L/2.,self.nx,endpoint=True),np.linspace(-L/2.,L/2.,self.nx,endpoint=True))
        self.im = np.zeros((self.nx,self.nx))
        for i in range(0,self.im.shape[0]):
            for j in range(0,self.im.shape[1]):
                    self.im[i,j] = self.pot.val(xx[i,j],yy[i,j])
        self.im = np.uint8(255.*(self.im/self.im.max()))
            
    def update_texture(self):
        L = 200
        dx = 1
        self.nx = int(L/dx)
        with self.plotbox.canvas:
            cx = self.plotbox.pos[0]
            cy = self.plotbox.pos[1]
            w = self.plotbox.size[0]
            h = self.plotbox.size[1]
            b = min(w,h)
            
            
            self.plot_texture.blit_buffer(self.im.reshape(self.im.size),colorfmt='luminance')
            Rectangle(texture = self.plot_texture, pos = (b/4.,cy),size = (b,b))
            print(w,h)
            print(cx,cy)
            
            
            
    def add_pot_list(self):
        self.potentials.append('Gauss:x0 = {}, y0 = {}, V0 = {}, Sig = {}'.format(round(self.param0,2),round(self.param1,2),round(self.param2,2),round(self.param3,2)))
        self.pot.add_function(gauss,dgaussx,dgaussy,[self.param0,self.param1,self.param2,self.param3])
        self.background()
        self.update_texture()
    def reset_pot_list(self):
        self.pot.clear()
        self.potentials = []
        self.plotbox.canvas.clear()
        
    def add_particle_list(self):
        self.particlestrings.append('P{}: m = {}, x0 = {}, y0 = {}, vx0 = {}, vy0 = {}'.format(len(self.particlestrings)+1,round(self.mass,2),round(self.x0,2),round(self.y0,2),round(self.vx0,2),round(self.vy0,2)))
        self.particles.append(Particle(self.mass,self.charge,np.ones([1,4]),dt))
        self.init_conds.append([self.x0,self.y0,self.vx0,self.vy0])
    def reset_particle_list(self):
        self.particlestrings = []
        self.particles = []
        self.init_conds = []
    
    def compute(self):
        for i,p in enumerate(self.particles,0):
            p.ComputeTrajectoryF(self.init_conds[i],self.pot)
        print('Done')
        for p in self.particles:
            print(p.trajectory[-1,:])
            
    def play(self):
        self.timer = Clock.schedule_interval(self.animate,0.04)
    
    def pause(self):
        self.timer.cancel()
        
    def animate(self,interval):
#        self.speed = 1.
        w = self.plotbox.size[0]
        h = self.plotbox.size[1]
        b = min(w,h)
        scalew = w/200.
        scaleh = h/200.
        self.plotbox.canvas.clear()
        self.update_texture()
        with self.plotbox.canvas:
            for p in self.particles:
                Color(1.0,1.0,1.0)
                Ellipse(pos=(p.trax(self.time)*scalew+w/2.,p.tray(self.time)*scaleh+h/2.),size=(10,10))
        if(self.time <= self.T):
            self.time += interval
        else:
            self.time = 0.
            
            
class simApp(App):

    def build(self):
        return main()


if __name__ == '__main__':
    simApp().run()