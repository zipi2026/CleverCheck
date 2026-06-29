import { Link } from 'react-router-dom';
import type { ExamCardModel } from '../../types';

type Props = {
  exam: ExamCardModel;
};

const statusLabel = (status: ExamCardModel['status']) => {
  switch (status) {
    case 'Active':
      return 'Active';
    case 'InProgress':
      return 'InProgress';
    case 'Submitted':
      return 'Submitted';
    case 'Graded':
      return 'Graded';
    default:
      return 'Closed';
  }
};

export const ExamCard = ({ exam }: Props) => {
  const actionText = exam.status === 'Submitted' || exam.status === 'Graded' ? 'View Results' : exam.status === 'InProgress' ? 'Continue Exam' : 'Start Exam';
  const destination = exam.status === 'Submitted' || exam.status === 'Graded' ? `/results/${exam.examId * 100}` : `/exam/${exam.examId}`;

  return (
    <article style={{ border: '1px solid #e5e7eb', borderRadius: 12, padding: 16, display: 'grid', gap: 8 }}>
      <h3 style={{ margin: 0 }}>{exam.name}</h3>
      <div>Subject: {exam.subject}</div>
      <div>Status: {statusLabel(exam.status)}</div>
      <div>Duration: {exam.durationMinutes} mins</div>
      <Link to={destination} style={{ justifySelf: 'start', padding: '8px 12px', background: '#2563eb', color: 'white', borderRadius: 8, textDecoration: 'none' }}>
        {actionText}
      </Link>
    </article>
  );
};
