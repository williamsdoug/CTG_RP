
import os
import numpy as np
import matplotlib.pyplot as plt
from pyts.image import RecurrencePlot
import imageio


def rp_norm(X_dist, threshold=None, percentage=10):
    """Rescale Recurrence Plot after setting nearest-neighbor threshold"""
    n_samples  = X_dist.shape[0]    # typically value is 1
    image_size = X_dist.shape[-1]

    assert threshold is not None

    if threshold == 'percentage_points':
        percents = np.percentile(
            np.reshape(X_dist, (n_samples, image_size * image_size)),
            percentage, axis=1
        )
        X_rp = X_dist < percents[:, None, None]
    if threshold == 'percentage_clipped':
        percents = np.percentile(
            np.reshape(X_dist, (n_samples, image_size * image_size)),
            percentage, axis=1
        )
        for i in range(n_samples):
            X_dist[i, X_dist[i] < percents[i]] = percents[i]
            X_dist[i] = percents[i] / X_dist[i]
        X_rp = X_dist**2
    elif threshold == 'percentage_distance':
        percents = percentage / 100 * np.max(X_dist, axis=(1, 2))
        X_rp = X_dist < percents[:, None, None]
    else:
        X_rp = X_dist < threshold
    return X_rp.astype('float64')


def np_to_uint8(X):
    X -= X.min()
    X = (255/X.max())*X
    return X.astype(np.uint8)


def create_rp(segment,
              dimension=2, time_delay=1, percentage=1, use_clip=False,
              images_dir='', base_name='Sample',
              suffix='jpg', # suffix='png'
              show_image=False, cmap=None, ##cmap='gray', cmap='binary'
             ):
    """Generate recurrence plot for specified signal segment and save to disk"""

    if base_name is None:
        base_name  = 'sample'
    fname = '{}_d{}_t{}_p{}{}.{}'.format(base_name, dimension, time_delay, percentage,
                                       '_clipped' if use_clip else '', suffix)

    segment = np.expand_dims(segment, 0)
    if use_clip:
        rp = RecurrencePlot(dimension=dimension, time_delay=time_delay)
        X_dist = rp.fit_transform(segment)
        X_rp = rp_norm(X_dist, threshold='percentage_clipped', percentage=percentage)
    else:
        rp = RecurrencePlot(dimension=dimension, time_delay=time_delay,
                            threshold='percentage_points', percentage=percentage)
        X_rp = rp.fit_transform(segment)

    X_rp = X_rp[0]  # remove leading dimension
    imageio.imwrite(os.path.join(images_dir, fname), np_to_uint8(X_rp))

    if show_image:
        plt.figure(figsize=(3, 3))
        plt.imshow(X_rp, cmap=cmap, origin='lower')
        plt.title('Recurrence Plot for {}'.format(fname), fontsize=14)
        plt.show()

    return fname
