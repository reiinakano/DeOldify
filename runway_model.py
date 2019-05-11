# MIT License

# Copyright (c) 2019 Runway AI, Inc

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import runway
from runway.data_types import number, image, category

from fasterai.visualize import get_image_colorizer, get_video_colorizer


@runway.setup(options={"architecture": category(choices=['Artistic', 'Stable', 'Video'], default='Artistic')})
def setup(opts):
    architecture = opts['architecture']
    print('[SETUP] Ran with architecture "{}"'.format(architecture))

    if architecture == 'Artistic':
        colorizer = get_image_colorizer(artistic=True)
    elif architecture == 'Stable':
        colorizer = get_image_colorizer(artistic=False)
    else:
        colorizer = get_video_colorizer().vis
    return colorizer


@runway.command(name='generate',
                inputs={ 'image': image(),
                         'render_factor': number(min=7, max=45, step=1, default=35) },
                outputs={ 'image': image() })
def generate(model, args):
    render_factor = args['render_factor']
    print('[GENERATE] Ran with render_factor "{}"'.format(render_factor))

    orig_image = args['image'].convert('RGB')
    model._clean_mem()
    output_image = model.filter.filter(orig_image, orig_image, render_factor=render_factor)

    return {
        'image': output_image
    }


if __name__ == '__main__':
    runway.run(host='0.0.0.0', port=8888)
