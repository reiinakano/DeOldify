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


architecture_description = "DeOldify model to use.\n" \
                           "Artistic achieves the highest quality results in image coloration, in terms of " \
                           "interesting details and vibrance. The most notable drawback however is that it's a bit " \
                           "of a pain to fiddle around with to get the best results.\n" \
                           "Stable achieves the best results with landscapes and portraits. Notably, it " \
                           "produces less 'zombies'- where faces or limbs stay gray rather than being colored " \
                           "in properly.\n" \
                           "Video is optimized for smooth, consistent and flicker-free video."

render_factor_description = "The default value of 35 has been carefully chosen and should work -ok- for most " \
                            "scenarios (but probably won't be the -best-). This determines resolution at which " \
                            "the color portion of the image is rendered. Lower resolution will render faster, and " \
                            "colors also tend to look more vibrant. Older and lower quality images in particular" \
                            " will generally benefit by lowering the render factor. Higher render factors are often " \
                            "better for higher quality images, but the colors may get slightly washed out."


@runway.setup(options={"architecture": category(description=architecture_description,
                                                choices=['Artistic', 'Stable', 'Video'],
                                                default='Artistic')})
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
                inputs={ 'image': image(description='Image to colorize'),
                         'render_factor': number(description=render_factor_description,
                                                 min=7, max=45, step=1, default=35) },
                outputs={ 'image': image(description='Colorized image') })
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
