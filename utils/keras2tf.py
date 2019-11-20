import tensorflow as tf
from tensorflow.python.framework import graph_io
from tensorflow.keras.models import load_model


# Clear any previous session.
tf.compat.v1.keras.backend.clear_session()

save_pb_dir = './unet/weights/weights_converted'
model_fname = './unet/weights/final_0.hdf5'

def freeze_graph(graph, session, output, save_pb_dir='.', save_pb_name='frozen_model.pb', save_pb_as_text=False):
    with graph.as_default():
        graphdef_inf = tf.compat.v1.graph_util.remove_training_nodes(graph.as_graph_def())
        graphdef_frozen = tf.compat.v1.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
        # graph_io.write_graph(graphdef_frozen, save_pb_dir, save_pb_name, as_text=save_pb_as_text)
        with tf.gfile.GFile(save_pb_dir+"/"+save_pb_name, "wb") as f:
            f.write(graphdef_frozen.SerializeToString())
        return graphdef_frozen

# This line must be executed before loading Keras model.
tf.keras.backend.set_learning_phase(0)

model = load_model(model_fname)

session =  tf.compat.v1.keras.backend.get_session()

INPUT_NODE = [t.op.name for t in model.inputs]
OUTPUT_NODE = [t.op.name for t in model.outputs]
print(INPUT_NODE, OUTPUT_NODE)
frozen_graph = freeze_graph(session.graph, session, [out.op.name for out in model.outputs], save_pb_dir=save_pb_dir)


mo_tf_path = '/opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py'

pb_file = '/home/mmatsi/SS/customNN/unet/weights/weights_converted/frozen_model.pb'
output_dir = '/home/mmatsi/SS/customNN/unet/weights/weights_converted/openvino'

input_shape = [1,480,640,3]
input_shape_str = str(input_shape).replace(' ','')
# input_shape_str

print(f"python3 {mo_tf_path} --input_model {pb_file} --output_dir {output_dir} --input_shape {input_shape_str} --data_type FP32")