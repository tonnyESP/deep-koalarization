import tensorflow as tf

from dataset.batching.single_image_record import ImageRecordReader

# Just for testing, reads and show images from a tfrecord
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    irr = ImageRecordReader('single_images.tfrecord')

    # Important: read_batch MUST be called before start_queue_runners,
    # otherwise the internal shuffle queue gets created but won't start
    key_batch, image_batch = irr.read_batch(50)

    key_one, img_one = irr.read_one()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        # Coordinate the loading of image files.
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)

        # Reading images sequentially one by one
        for i in range(15):
            k, image = sess.run([key_one, img_one])
            plt.subplot(3, 5, i + 1)
            plt.imshow(image)
            plt.axis('off')
            print('Read', k)
        plt.show()

        # Reading images in a batch of 50
        keys, imgs = sess.run([key_batch, image_batch])
        print(keys, imgs.shape)

        # Finish off the filename queue coordinator.
        coord.request_stop()
        coord.join(threads)