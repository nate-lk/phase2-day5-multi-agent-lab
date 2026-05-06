# Lab Guide: Multi-Agent Research System

## Scenario
Bạn cần xây dựng một research assistant có thể nhận câu hỏi dài, tìm thông tin, phân tích và viết câu trả lời cuối cùng. Lab yêu cầu so sánh hai cách làm:

1. **Single-agent baseline**: một agent làm toàn bộ.
2. **Multi-agent workflow**: Supervisor điều phối Researcher, Analyst, Writer.

## Quy tắc quan trọng
- Không thêm agent nếu không có lý do rõ ràng.
- Mỗi agent phải có responsibility riêng.
- Shared state phải đủ rõ để debug.
- Phải có trace hoặc log cho từng bước.
- Phải benchmark, không chỉ nhìn output bằng cảm tính.

## Milestone 1: Baseline
✅ **Completed**: Single-agent implementation is available via `python -m multi_agent_research_lab.cli baseline`.

## Milestone 2: Supervisor
✅ **Completed**: Routing policy is implemented in `supervisor.py` using a state-based decision logic.

## Milestone 3: Worker agents
✅ **Completed**: `ResearcherAgent`, `AnalystAgent`, and `WriterAgent` are implemented with specialized prompts and tool access.

## Milestone 4: Trace và benchmark
✅ **Completed**: Automated benchmarking system compares single vs. multi-agent across Latency, Cost, and Quality.

## Exit ticket

**1. Case nào nên dùng multi-agent? Vì sao?**
- **Nghiên cứu chuyên sâu (In-depth research)**: Khi bài toán đòi hỏi nhiều bước xử lý riêng biệt (tìm kiếm, đối soát, viết lách). Chia nhỏ task giúp giảm tải context cho LLM và cho phép kiểm soát chất lượng (guardrails) ở từng giai đoạn.
- **Quy trình cần sự khách quan (Objective review)**: Khi cần một agent khác (như Critic) để phản biện hoặc kiểm tra chéo (hallucination check) kết quả của agent trước đó.

**2. Case nào không nên dùng multi-agent? Vì sao?**
- **Task đơn giản (Low complexity)**: Các yêu cầu có thể trả lời trực tiếp trong 1 prompt (ví dụ: "Thủ đô của Pháp là gì?"). Dùng multi-agent sẽ gây lãng phí latency và tiền bạc (token cost).
- **Yêu cầu phản hồi thời gian thực (Real-time latency)**: Khi người dùng cần câu trả lời ngay lập tức. Multi-agent có độ trễ cao do phải thực hiện nhiều call LLM tuần tự.
