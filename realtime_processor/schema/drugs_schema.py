from pyspark.sql.types import StructType, StructField, StringType, TimestampType


def get_drugs_schema():
    return StructType([
        StructField("idThuoc", StringType(), True),
        StructField("phanLoaiThuocEnum", StringType(), True),
        StructField("tenCongTyDangKy", StringType(), True),
        StructField("diaChiDangKy", StringType(), True),
        StructField("nuocDangKy", StringType(), True),
        StructField("congTyDangKyId", StringType(), True),
        StructField("tenCongTySanXuat", StringType(), True),
        StructField("diaChiSanXuat", StringType(), True),
        StructField("nuocSanXuat", StringType(), True),
        StructField("congTySanXuatId", StringType(), True),
        StructField("fullAddress", StringType(), True),
        StructField("soDangKy", StringType(), True),  # PRIMARY KEY, so it cannot be null
        StructField("soDangKyCu", StringType(), True),
        StructField("tenThuoc", StringType(), True),
        StructField("dotCap", StringType(), True),
        StructField("ngayCapSoDangKy", TimestampType(), True),
        StructField("ngayHetHanSoDangKy", TimestampType(), True),
        StructField("ngayGiaHanSoDangKy", TimestampType(), True),
        StructField("soQuyetDinh", StringType(), True),
        StructField("thongTinRutSoDangKy", StringType(), True),
        StructField("dangBaoChe", StringType(), True),
        StructField("dongGoi", StringType(), True),
        StructField("hamLuong", StringType(), True),
        StructField("hoatChatChinh", StringType(), True),
        StructField("tieuChuan", StringType(), True),
        StructField("tieuChuanId", StringType(), True),
        StructField("tuoiTho", StringType(), True),
        StructField("creationTime", TimestampType(), True),
        StructField("lastModificationTime", TimestampType(), True),
        StructField("crawlTime", TimestampType(), True)
    ])