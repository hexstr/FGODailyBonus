using System;
using System.Text;
using System.Linq;
using System.IO;
using System.Security.Cryptography;

class CertificateExtractor {
  static void Main() {
    string YourCertificate = "ZSv/WkOGiQ25eqY+A5Lgln3pq91NidrEBM/BezdP0gbYJFS6y";
	byte[] bytes = new byte[] { 0x62,0x35,0x6e,0x48,0x6a,0x73,0x4d,0x72,0x71,0x61,0x65,0x4e,0x6c,0x69,0x53,0x73,0x33,0x6a,0x79,0x4f,0x7a,0x67,0x70,0x44 };
	byte[] bytes2 = new byte[] { 0x77,0x75,0x44,0x36,0x6b,0x65,0x56,0x72 };
	TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
	byte[] result;
	using (MemoryStream memoryStream = new MemoryStream())
	{
		using (CryptoStream cryptoStream = new CryptoStream(memoryStream, tripleDESCryptoServiceProvider.CreateDecryptor(bytes, bytes2), CryptoStreamMode.Write))
		{
			cryptoStream.Write(Convert.FromBase64String(YourCertificate), 0, 0xB8);
			cryptoStream.Close();
		}
		result = memoryStream.ToArray();
		memoryStream.Close();
	}
	Console.WriteLine(Encoding.UTF8.GetString(result));
  }
}