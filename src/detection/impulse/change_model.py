import tensorflow as tf
import binascii

impulse_mode_path = "model/impulse.lite"
# # TensorFlow Liteモデルに変換
# #
# interpreter = tf.lite.Interpreter(model_path=impulse_mode_path)
# interpreter.allocate_tensors()


# with open("model/impulse.tflite", "wb") as f:
#     f.write(interpreter._get_model_content())
def convert_to_c_array(bytes) -> str:
    hexstr = binascii.hexlify(bytes).decode("UTF-8")
    hexstr = hexstr.upper()
    array = ["0x" + hexstr[i : i + 2] for i in range(0, len(hexstr), 2)]
    array = [array[i : i + 10] for i in range(0, len(array), 10)]
    return ",\n  ".join([", ".join(e) for e in array])


tflite_binary = open(impulse_mode_path, "rb").read()
ascii_bytes = convert_to_c_array(tflite_binary)
header_file = (
    "const unsigned char model_tflite[] = {\n  "
    + ascii_bytes
    + "\n};\nunsigned int model_tflite_len = "
    + str(len(tflite_binary))
    + ";"
)
open("model/impulse.h", "w").write(header_file)
