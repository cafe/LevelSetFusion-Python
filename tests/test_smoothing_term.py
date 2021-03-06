#  ================================================================
#  Created by Gregory Kramida on 10/17/18.
#  Copyright (c) 2018 Gregory Kramida
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

from unittest import TestCase
import numpy as np
from nonrigid_opt import smoothing_term as st
from utils.tsdf_set_routines import set_zeros_for_values_outside_narrow_band_union


# NOTE: expected energies are different, since the vectorized version uses forward/backward differences at
# the boundaries as appropriate, while the non-vectorized version simply replicates values at the border and
# uses central differences. Technically, using central differences is better-reflective of the way the
# gradients are computed, but for a large-enough field, this makes close to no difference, especially
# considering the energy value is just used as a heuristic to analyze convergence progress.


class SmoothingTermTest(TestCase):
    def test_smoothing_term01(self):
        warp_field = np.array([[[0., 0.], [1., 1.]],
                               [[1., 1.], [1., 1.]]], dtype=np.float32)

        live_field = np.array([[0.3, 0.5],
                               [-0.8, 1.]])
        canonical_field = np.array([[0.5, -0.3],
                                    [1., 0.]])

        expected_gradient_out = np.array([[[-2., -2.], [1., 1.]],
                                          [[1., 1.], [0., 0.]]], dtype=np.float32)
        expected_energy_out = 1.0

        gradient_out, energy_out = st.compute_smoothing_term_gradient_direct(warp_field, live_field, canonical_field)

        self.assertTrue(np.allclose(gradient_out, expected_gradient_out))
        self.assertEqual(energy_out, expected_energy_out)

        gradient_out = st.compute_smoothing_term_gradient_vectorized(warp_field)
        energy_out = st.compute_smoothing_term_energy(warp_field, live_field, canonical_field)

        # See note at top of file on why expected energies are different for the vectorized/non-vectorized version
        expected_energy_out = 4.0

        self.assertTrue(np.allclose(gradient_out, expected_gradient_out))
        self.assertEqual(energy_out, expected_energy_out)

    def test_smoothing_term02(self):
        warped_live_field = np.array([[1., 1., 0.49999955],
                                      [1., 0.44999936, 0.34999937],
                                      [1., 0.35000065, 0.25000066]], dtype=np.float32)
        canonical_field = np.array([[1.0000000e+00, 1.0000000e+00, 3.7499955e-01],
                                    [1.0000000e+00, 3.2499936e-01, 1.9999936e-01],
                                    [1.0000000e+00, 1.7500064e-01, 1.0000064e-01]], dtype=np.float32)

        warp_field = np.array([[[0., 0.],
                                [0., 0.],
                                [-0.3, -0.2]],

                               [[0., 0.],
                                [-0.40, -0.40],
                                [-0.1, -0.2]],

                               [[0., 0.],
                                [-0.6, -0.2],
                                [-0.1, -0.1]]], dtype=np.float32)

        expected_gradient_out = np.array([[[0., 0.],
                                           [0., 0.],
                                           [-0.5, -0.2]],

                                          [[0., 0.],
                                           [-0.9, -1.2],
                                           [0.5, 0.1]],

                                          [[0., 0.],
                                           [-1.3, -0.1],
                                           [0.5, 0.2]]], dtype=np.float32)
        expected_energy_out = 0.14625

        smoothing_gradient_out, smoothing_energy_out = \
            st.compute_smoothing_term_gradient_direct(warp_field, warped_live_field, canonical_field)

        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        self.assertAlmostEqual(smoothing_energy_out, expected_energy_out, places=6)

        smoothing_gradient_out = st.compute_smoothing_term_gradient_vectorized(warp_field)
        set_zeros_for_values_outside_narrow_band_union(warped_live_field, canonical_field, smoothing_gradient_out)
        smoothing_energy_out = st.compute_smoothing_term_energy(warp_field, warped_live_field, canonical_field)

        # See note at top of file on why expected energies are different for the vectorized/non-vectorized version
        expected_energy_out = 0.39

        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        self.assertAlmostEqual(smoothing_energy_out, expected_energy_out, places=6)

    def test_smoothing_term03(self):
        warped_live_field = np.array([[1., 1., 0.49999955, 0.42499956],
                                      [1., 0.44999936, 0.34999937, 0.32499936],
                                      [1., 0.35000065, 0.25000066, 0.22500065],
                                      [1., 0.20000044, 0.15000044, 0.07500044]], dtype=np.float32)
        canonical_field = np.array([[1.0000000e+00, 1.0000000e+00, 3.7499955e-01, 2.4999955e-01],
                                    [1.0000000e+00, 3.2499936e-01, 1.9999936e-01, 1.4999935e-01],
                                    [1.0000000e+00, 1.7500064e-01, 1.0000064e-01, 5.0000645e-02],
                                    [1.0000000e+00, 7.5000443e-02, 4.4107438e-07, -9.9999562e-02]], dtype=np.float32)

        warp_field = np.array([[[0., 0.],
                                [0., 0.],
                                [-0.35937524, -0.18750024],
                                [-0.13125, -0.17500037], ],

                               [[0., 0.],
                                [-0.4062504, -0.4062496],
                                [-0.09375, -0.1874992],
                                [-0.04375001, -0.17499907], ],

                               [[0., 0.],
                                [-0.65624946, -0.21874908],
                                [-0.09375, -0.1499992],
                                [-0.04375001, -0.21874908], ],

                               [[0., 0.],
                                [-0.5312497, -0.18750025],
                                [-0.09374999, -0.15000032],
                                [-0.13125001, -0.2625004], ]], dtype=np.float32)

        expected_gradient_out = np.array([[[0., 0.],
                                           [0., 0.],
                                           [-0.8531257, -0.20000115],
                                           [0.14062527, 0.01249856]],

                                          [[0., 0.],
                                           [-0.8750021, -1.2187502],
                                           [0.52812564, 0.16875133],
                                           [0.13749997, 0.05625144]],

                                          [[0., 0.],
                                           [-1.5937477, -0.13124725],
                                           [0.51249945, 0.17500085],
                                           [0.13749999, -0.06874855]],

                                          [[0., 0.],
                                           [-0.8437496, -0.19375136],
                                           [0.47499973, 0.14999892],
                                           [-0.125, -0.1562514]]], dtype=np.float32)

        expected_energy_out = 0.2126010925276205

        smoothing_gradient_out, energy_out = \
            st.compute_smoothing_term_gradient_direct(warp_field, warped_live_field, canonical_field)

        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        self.assertAlmostEqual(energy_out, expected_energy_out, places=6)

        smoothing_gradient_out = st.compute_smoothing_term_gradient_vectorized(warp_field)
        set_zeros_for_values_outside_narrow_band_union(warped_live_field, canonical_field, smoothing_gradient_out)
        energy_out = st.compute_smoothing_term_energy(warp_field, warped_live_field, canonical_field)

        # See note at top of file on why expected energies are different for the vectorized/non-vectorized version
        expected_energy_out = 0.2802989184856415

        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        self.assertAlmostEqual(energy_out, expected_energy_out, places=6)

    def test_smoothing_term04(self):
        # @formatter:off
        warp_field = np.array(
            [0, 0, -0, -0, -0.0338037, -0.0174936, -0.0112804, -0.0191113,
             -0, 0, -0.0379127, -0.0383908, -0.00838349, -0.0181314, -0.00353384, -0.0182579,
             -0, 0, -0.061653, -0.0186044, -0.00832757, -0.0134227, -0.00379325, -0.0187587,
             -0, 0, -0.0580528, -0.0173559, -0.00826604, -0.0136066, -0.0109505, -0.0239675],
            dtype=np.float32).reshape(4, 4, 2)

        warped_live_field = np.array(
            [1, 1, 0.519703, 0.443642,
             1, 0.482966, 0.350619, 0.329146,
             1, 0.381416, 0.249635, 0.227962,
             1, 0.261739, 0.166676, 0.117205], np.float32).reshape(4, 4)

        canonical_field = np.array(
            [-1, 1, 0.375, 0.25,
             -1, 0.324999, 0.199999, 0.149999,
             1, 0.175001, 0.100001, 0.0500006,
             1, 0.0750004, 4.41074e-07, -0.0999996], np.float32).reshape(4, 4)
        # @formatter:on

        smoothing_gradient_out = st.compute_smoothing_term_gradient_vectorized(warp_field)
        set_zeros_for_values_outside_narrow_band_union(warped_live_field, canonical_field, smoothing_gradient_out)
        energy_out = st.compute_smoothing_term_energy(warp_field, warped_live_field, canonical_field)

        expected_gradient_out = np.array([[[[[0., 0.],
                                             [0., 0.],
                                             [-0.08174722, -0.0152381],
                                             [0.01477674, -0.0024711]],

                                            [[0., 0.],
                                             [-0.08161432, -0.11682741],
                                             [0.05004385, 0.0150394],
                                             [0.01285562, 0.0012277]],

                                            [[0., 0.],
                                             [-0.14231893, -0.0052482],
                                             [0.0487855, 0.0154103],
                                             [0.01143216, -0.000628]],

                                            [[0., 0.],
                                             [-0.10423936, -0.0198567],
                                             [0.05253275, 0.0139263],
                                             [-0.00984171, -0.0155697]]]]], dtype=np.float32)
        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        self.assertAlmostEqual(0.002550773788243532, energy_out)

        smoothing_gradient_out, energy_out = \
            st.compute_smoothing_term_gradient_direct(warp_field, warped_live_field, canonical_field)
        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        # See note at top of file on why expected energies are different for the vectorized/non-vectorized version
        self.assertAlmostEqual(0.001989291487916489, energy_out)

    def test_smoothing_term05(self):
        # corresponds to test_tikhonov_regularization_gradient02 for C++
        grad = np.array([[[0., 0.],
                          [-0., -0.],
                          [-0.33803707, -0.17493579],
                          [-0.11280416, -0.1911128]],  # row 1

                         [[-0.0, 0.],
                          [-0.37912705, -0.38390793],
                          [-0.08383488, -0.1813143],
                          [-0.03533841, -0.18257865]],  # row 2

                         [[-0., 0.],
                          [-0.61653014, -0.18604389],
                          [-0.08327565, -0.13422713],
                          [-0.03793251, -0.18758682]],  # row 3

                         [[-0., 0.],
                          [-0.58052848, -0.17355914],
                          [-0.0826604, -0.13606551],
                          [-0.10950545, -0.23967532]]], dtype=np.float32)

        warp_field = grad * 0.1
        expected_gradient_out = np.array(
            [[[-0., -0.],
              [0.07171641, 0.05588437],
              [-0.08174722, -0.01523803],
              [0.01477672, -0.00247112]],

             [[0.0379127, 0.03839079],
              [-0.08161432, -0.11682735],
              [0.05004386, 0.01503923],
              [0.01285563, 0.0012278]],

             [[0.06165301, 0.01860439],
              [-0.14231894, -0.00524814],
              [0.04878554, 0.0154102],
              [0.0114322, -0.00062794]],

             [[0.05805285, 0.01735591],
              [-0.10423949, -0.0198568],
              [0.05253284, 0.01392651],
              [-0.0098418, -0.01556983]]], dtype=np.float32)
        smoothing_gradient_out = st.compute_smoothing_term_gradient_vectorized(warp_field)
        energy_out = st.compute_smoothing_term_energy(warp_field, band_union_only=False)

        self.assertTrue(np.allclose(smoothing_gradient_out, expected_gradient_out))
        self.assertAlmostEqual(energy_out, 0.009552381932735443)
