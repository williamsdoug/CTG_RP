
import os
import numpy as np
import matplotlib.pyplot as plt
from pyts.image import RecurrencePlot
import imageio



def create_rp(segment,
              dimension=2, time_delay=1, percentage=1, use_clip=False, knn=None, imsize=None,
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
    if knn is not None:
        rp = RecurrencePlot(dimension=dimension, time_delay=time_delay)
        X_dist = rp.fit_transform(segment)[0]
        X_rp = mask_knn(X_dist, k=knn, policy='cols')
    elif use_clip:
        rp = RecurrencePlot(dimension=dimension, time_delay=time_delay)
        X_dist = rp.fit_transform(segment)
        X_rp = rp_norm(X_dist, threshold='percentage_clipped', percentage=percentage)[0]
    else:
        rp = RecurrencePlot(dimension=dimension, time_delay=time_delay,
                            #threshold='percentage_points', percentage=percentage)
                            threshold='point', percentage=percentage)
        X_rp = rp.fit_transform(segment)[0]

    if imsize is not None:
        X_rp = resize_rp(X_rp, new_shape=imsize, use_max=True)

    imageio.imwrite(os.path.join(images_dir, fname), np_to_uint8(X_rp))
    if show_image:
        plt.figure(figsize=(3, 3))
        plt.imshow(X_rp, cmap=cmap, origin='lower')
        plt.title('Recurrence Plot for {}'.format(fname), fontsize=14)
        plt.show()
    return fname


def np_to_uint8(X):
    X -= X.min()
    X = (255/X.max())*X
    return X.astype(np.uint8)


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


def mask_knn(m, k=1, policy='cols'):
    """Creates mask showing knn in each row/column of adjacency matrix"""
    assert policy in ['cols', 'rows']
    mask = np.zeros(m.shape, dtype='bool')
    if policy == 'rows':
        assert m.shape[0] >= k
        vals = np.partition(m, k+1, axis=1)[:, k]  # kth value in each row
        for i in range(m.shape[0]):
            mask[i][m[i] <= vals[i]] = True
    else:
        assert m.shape[1] >= k
        vals = np.partition(m, k+1, axis=0)[k, :]  # kth value in each column
        for i in range(m.shape[1]):
            mask[:, i][m[:, i] <= vals[i]] = True
    return mask


def compute_padding(w, n_align=64):
    """compute required padding for given dimension to naturally align"""
    if w % n_align > 0:
        new_w = ((w // n_align) + 1) * n_align
    else:
        new_w = w
    pad = new_w - w
    pad_l = pad // 2
    pad_r = pad - pad_l
    return new_w, pad_l, pad_r


def align_rp(m, n_align=64):
    """Apply padding to align matrix to given multiple"""
    rows, cols = m.shape

    new_rows, pad_rows_l, pad_rows_r = compute_padding(rows, n_align)
    new_cols, pad_cols_l, pad_cols_r = compute_padding(cols, n_align)
    if rows == new_rows and cols == new_cols:
        padded_m = m
    else:
        padded_m = np.zeros((new_rows,new_cols), dtype=bool)

        if rows == new_rows:
            padded_m[:, pad_cols_l:-pad_cols_r] = a
        elif cols == new_cols:
            padded_m[pad_rows_l:-pad_rows_r, :] = a
        else:
            print('')
            print(padded_m.shape)
            print(padded_m[pad_rows_l:-pad_rows_r, pad_cols_l:-pad_cols_r].shape)
            padded_m[pad_rows_l:-pad_rows_r, pad_cols_l:-pad_cols_r] = m
    return padded_m


def resize_rp(mat, new_shape=64, use_mean=False):
    mat = align_rp(mat, n_align=new_shape)

    rows, cols = mat.shape[0], mat.shape[1]
    downscale_row, downscale_col = rows // new_shape, cols // new_shape
    if use_mean:
        result = np.zeros((new_shape, new_shape))
        for i, ii in enumerate(range(0, rows, downscale_row)):
            for j, jj in enumerate(range(0, cols, downscale_col)):
                result[i, j] = np.mean(mat[ii:ii + downscale_row, jj:jj + downscale_col])
    else:
        result = np.zeros((new_shape, new_shape), dtype=bool)
        for i, ii in enumerate(range(0, rows, downscale_row)):
            for j, jj in enumerate(range(0, cols, downscale_col)):
                result[i, j] = np.max(mat[ii:ii + downscale_row, jj:jj + downscale_col])
    return result
