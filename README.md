# Still Working

## Background
My diploma project is to make some improvements on [DeepPoly](https://github.com/eth-sri/eran)
and use it to test some other DNNs.

## First Step
Since DeepPoly only support MNIST and CIFAR-10 for now, l want to generalize its code so that
it can handle more Image-Classify Problems.

So l trained a CNN by using the dataset from <http://www.robots.ox.ac.uk/~vgg/data/>.
To simplify this problem, l only use six kinds of flowers. Another reason for the 'six' is
that my network is from <https://www.coursera.org/learn/convolutional-neural-networks/home/welcome>.
So thanks Andrew here.

You also can download the entire `dataset`(17flowers.tgz) there.

## Second Step
Only in safety critical domains can DeepPoly show its importance. So 
l want to use it to test autonomous driving network. And l 
use the models that are mentioned in <https://arxiv.org/abs/1802.02295>
and also open in [github](https://github.com/udacity/self-driving-car).
But l am encountering great difficulty because these networks are not used
to classify images, but used to predict driving-angles which means they will only
generate a real value. So l will change the code in DeepPoly so that it 
can handle these networks.`Wish me luck`.