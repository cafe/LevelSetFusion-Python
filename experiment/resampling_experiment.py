#  ================================================================
#  Created by Gregory Kramida on 1/22/19.
#  Copyright (c) 2019 Gregory Kramida
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ================================================================

import sys
import math_utils.elliptical_gaussians as eg
import math
import numpy as np

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1


def main():
    ellipse0 = eg.implicit_ellipse_from_radii_and_angle(1, 2, 0, 1)
    ellipse1 = eg.implicit_ellipse_from_radii_and_angle(1, 2, math.pi / 2, 1)
    ellipse2 = eg.implicit_ellipse_from_radii_and_angle(1, 2, math.pi / 4, 1)

    gaussian = eg.EllipticalGaussian(ellipse2)
    gaussian.visualize()


    #ellipse2.visualize(scale=100, margin=5)


    # print(ellipse0.get_tight_bounds())
    # print(ellipse1.get_tight_bounds())
    # print(ellipse2.get_tight_bounds())

    #print(ellipse0.get_bounds1())
    #print(ellipse1.get_bounds1())
    #print(ellipse2.get_bounds1())

    return EXIT_CODE_SUCCESS


if __name__ == "__main__":
    sys.exit(main())