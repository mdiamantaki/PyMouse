from core.Stimulus import *
from utils.Presenter import *

@stimulus.schema
class Dot(Stimulus, dj.Manual):
    definition = """
    # This class handles the presentation of area mapping Bar stimulus
    -> StimCondition
    ---
    bg_level              : tinyblob  # 0-255 
    dot_level             : tinyblob  # 0-255 
    dot_x                 : float  # (fraction of monitor width, 0 for center, from -0.5 to 0.5) position of dot on x axis
    dot_y                 : float  # (fraction of monitor width, 0 for center) position of dot on y axis
    dot_xsize             : float  # fraction of monitor width, width of dots
    dot_ysize             : float # fraction of monitor width, height of dots
    dot_shape             : enum('rect','oval') # shape of the dot
    dot_time              : float # (sec) time of each dot persists
    """

    cond_tables = ['Dot']
    required_fields = ['dot_x', 'dot_y', 'dot_xsize', 'dot_ysize', 'dot_time']
    default_key =  {'bg_level'              : 255,
                    'dot_level'             : 0,  # degrees
                    'dot_shape'             : 'rect'}

    def init(self, exp):
        self.fill_colors.background = (0, 0, 0)
        super().init(exp)
        self.size = (self.monitor['resolution_x'], self.monitor['resolution_y'])
        self.fps = self.monitor['fps']

        # setup pygame
        self.clock = pygame.time.Clock()
        self.Presenter = Presenter(self.monitor, background_color=self.fill_colors.background)

    def prepare(self, curr_cond):
        self.curr_cond = curr_cond
        self.fill_colors.background = self.curr_cond['bg_level']
        self.Presenter.set_background_color(self.curr_cond['bg_level'])
        #self.fill(self.curr_cond['bg_level'])
        width = self.monitor['resolution_x']
        height = self.monitor['resolution_y']
        x_start = self.curr_cond['dot_x'] * 2
        y_start = self.curr_cond['dot_y'] * 2 * width/height
        self.rect = (x_start - self.curr_cond['dot_xsize'],
                     y_start - self.curr_cond['dot_ysize']*width/height,
                     x_start + self.curr_cond['dot_xsize'],
                     y_start + self.curr_cond['dot_ysize']*width/height)

    def start(self):
        super().start()
        self.Presenter.draw_rect(self.rect, self.curr_cond['dot_level'])

    def stop(self):
        self.log_stop()
        self.isrunning = False

    def present(self):
        if self.timer.elapsed_time() > self.curr_cond['dot_time']*1000:
            self.isrunning = False

    def fill(self, color=False):
        if not color:
            color = self.fill_colors.background
        if self.fill_colors.background: self.Presenter.fill(color)

    def exit(self):
        self.Presenter.quit()


