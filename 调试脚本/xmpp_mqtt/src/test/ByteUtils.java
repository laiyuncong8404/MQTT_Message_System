package test;

public class ByteUtils {
	private static String hexString="0123456789ABCDEF";

	/**
	 * convet string to hex
	 */
	public static String string2Hex(String content) {
		byte[] bytes = content.getBytes();
		StringBuilder sb = new StringBuilder(bytes.length * 2);
		for(int i = 0; i < bytes.length; i++) {
			sb.append(hexString.charAt((bytes[i]&0xf0)>>4));
			sb.append(hexString.charAt((bytes[i]&0x0f)>>0));
		}
		return sb.toString();
	}
	
	public static String bytesToHexString(byte[] src) {
		StringBuilder stringBuilder = new StringBuilder("");
		if (src == null || src.length <= 0) {
			return null;
		}
		for (int i = 0; i < src.length; i++) {
			int v = src[i] & 0xFF;
			String hv = Integer.toHexString(v);
			if (hv.length() < 2) {
				stringBuilder.append(0);
			}
			stringBuilder.append(hv);
		}
		return stringBuilder.toString();
	}
	
	/**
	 * convet short to two bytes
	 */
	public static byte[] shortToBytes(short num) {
		byte[] byteNum = new byte[]{(byte)((num>>8)&0xFF), (byte)(num&0xFF)};
	    return byteNum;
	} 
	
	/**
	 * convert integer to one bytes
	 */
	public static byte intToByte(int integer) {
		String hexStr = Integer.toHexString(integer);
		return Byte.valueOf(hexStr, 16);
	} 
	
	/**
	 * convert integer to one bytes
	 */
	public static byte int2OneByte(int num) {
		return (byte) (num & 0x000000ff);
	}
	
	/**
	 * convert integer to four bytes
	 */
	public static byte[] int2Bytes(int num) {
		byte[] byteNum = new byte[4];
		for (int ix = 0; ix < 4; ++ix) {
			int offset = 32 - (ix + 1) * 8;
			byteNum[ix] = (byte) ((num >> offset) & 0xff);
		}
		return byteNum;
	}

	/**
	 * convert two bytes to int
	 */
	public static int twoBytes2Int(byte[] buffer) {
		return buffer[0] | buffer[1] << 8;
	}

	/**
	 * convert four bytes to int
	 */
	public static int bytes2Int(byte[] byteNum) {
		int num = 0;
		for (int ix = 0; ix < 4; ++ix) {
			num <<= 8;
			num |= (byteNum[ix] & 0xff);
		}
		return num;
	}

	/**
	 * convert four bytes to int
	 */
	public static int oneByte2Int(byte byteNum) {
		return byteNum & 0xFF;
	}

	public static byte[] long2Bytes(long num) {
		byte[] byteNum = new byte[8];
		for (int ix = 0; ix < 8; ++ix) {
			int offset = 64 - (ix + 1) * 8;
			byteNum[ix] = (byte) ((num >> offset) & 0xff);
		}
		return byteNum;
	}

	public static long bytes2Long(byte[] byteNum) {
		long num = 0;
		for (int ix = 0; ix < 8; ++ix) {
			num <<= 8;
			num |= (byteNum[ix] & 0xff);
		}
		return num;
	}
	
	public static int byteToInt16(byte b) {
		String result = Integer.toHexString(b & 0xFF); 
		return Integer.valueOf(result, 16);
	}
	
	public static boolean byteCompare(byte[] data1, byte[] data2, int len) {
		if (data1 == null && data2 == null) {
			return true;
		}
		if (data1 == null || data2 == null) {
			return false;
		}
		if (data1 == data2) {
			return true;
		}
		boolean bEquals = true;
		int i;
		for (i = 0; i < data1.length && i < data2.length && i < len; i++) {
			if (data1[i] != data2[i]) {
				bEquals = false;
				break;
			}
		}
		return bEquals;
	}
	
	public static String byteToBit(byte b) {  
	    return "" +(byte)((b >> 7) & 0x1) +   
	    (byte)((b >> 6) & 0x1) +   
	    (byte)((b >> 5) & 0x1) +   
	    (byte)((b >> 4) & 0x1) +   
	    (byte)((b >> 3) & 0x1) +   
	    (byte)((b >> 2) & 0x1) +   
	    (byte)((b >> 1) & 0x1) +   
	    (byte)((b >> 0) & 0x1);  
	} 

	public static byte[] intToByteArray(final int integer) {
		int byteNum = (40 - Integer.numberOfLeadingZeros(integer < 0 ? ~integer
				: integer)) / 8;
		byte[] byteArray = new byte[4];

		for (int n = 0; n < byteNum; n++)
			byteArray[3 - n] = (byte) (integer >>> (n * 8));

		return (byteArray);
	}
	
	public static short byteToShort(byte[] b) {
		short s = 0;
		short s0 = (short) (b[0] & 0xff);// �?���?
		short s1 = (short) (b[1] & 0xff);
		s1 <<= 8;
		s = (short) (s0 | s1);
		return s;
	}

	public static byte[] shortToByte(short number) {
		int temp = number;
		byte[] b = new byte[2];
		for (int i = 0; i < b.length; i++) {
			b[i] = new Integer(temp & 0xff).byteValue();// 将最低位保存在最低位 
			temp = temp >> 8; // 向右�?�?
		}
		return b;
	}
}
