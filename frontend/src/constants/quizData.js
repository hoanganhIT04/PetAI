// Các key lưu trữ LocalStorage
export const STORAGE_RESULTS_KEY = 'pet_recommend_results';
export const STORAGE_ANSWERS_KEY = 'pet_recommend_answers';

// Trọng số cho thuật toán so khớp (Càng cao thì tiêu chí đó càng quan trọng)
export const MATCHING_WEIGHTS = {
    energy: 2.0,       // Năng lượng là yếu tố then chốt nhất
    space: 1.5,        // Không gian sống quan trọng thứ hai
    kid_friendly: 1.8, // Thân thiện trẻ em được ưu tiên cao để đảm bảo an toàn
    grooming: 1.0      // Chăm sóc lông có trọng số thấp hơn
};

// Cấu trúc bộ câu hỏi
export const QUESTIONS = [
    {
        key: 'type',
        category: 'Loại thú cưng',
        subtitle: 'Chọn giữa chó hoặc mèo',
        text: 'Bạn muốn nuôi gì?',
        options: [
            { text: 'Chó', value: 'dog' },
            { text: 'Mèo', value: 'cat' }
        ]
    },
    {
        key: 'energy',
        category: 'Mức năng lượng',
        subtitle: 'Ảnh hưởng đến việc vận động mỗi ngày',
        text: 'Bạn thích thú cưng vận động mức nào?',
        options: [
            // Áp dụng Range Matching (Logic mờ) để tăng tỷ lệ Recall
            { text: 'Ít vận động', value: [1, 2] },
            { text: 'Trung bình', value: [3] },
            { text: 'Rất năng động', value: [4, 5] }
        ]
    },
    {
        key: 'space',
        category: 'Không gian sống',
        subtitle: 'Phù hợp với diện tích nhà',
        text: 'Không gian sống của bạn?',
        options: [
            { text: 'Nhỏ', value: [1, 2] },
            { text: 'Vừa', value: [3] },
            { text: 'Rộng', value: [4, 5] }
        ]
    },
    {
        key: 'grooming',
        category: 'Chăm sóc',
        subtitle: 'Thời gian bạn dành để chăm thú cưng',
        text: 'Bạn có thể chăm sóc lông mức nào?',
        options: [
            { text: 'Ít chăm', value: [1, 2] },
            { text: 'Bình thường', value: [3] },
            { text: 'Chăm kỹ', value: [4, 5] }
        ]
    },
    {
        key: 'kid_friendly',
        category: 'Gia đình',
        subtitle: 'Mức độ thân thiện với trẻ nhỏ',
        text: 'Nhà bạn có trẻ nhỏ không?',
        options: [
            // Lưu ý: kid_friendly điểm 1 là rất dữ, 5 là rất hiền. 
            // Nếu nhà có trẻ em, chỉ chấp nhận những loài hiền (4 hoặc 5)
            { text: 'Không có trẻ', value: [1, 2] },
            { text: 'Không quan trọng', value: [3] },
            { text: 'Có, cần rất hiền', value: [4, 5] }
        ]
    },
    {
        key: 'size',
        category: 'Kích thước',
        subtitle: 'Chọn kích thước thú cưng mong muốn',
        text: 'Bạn thích kích thước nào?',
        options: [
            // Size là dạng Category (Phân loại chữ) nên vẫn giữ nguyên String
            { text: 'Nhỏ', value: 'small' },
            { text: 'Trung bình', value: 'medium' },
            { text: 'Lớn', value: 'large' }
        ]
    }
];