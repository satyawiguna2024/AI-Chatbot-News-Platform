import { useMutation } from "@tanstack/react-query";
import { createConversation, deleteConversation } from "@/lib/api/chat";

export const useCreateConversation = () => useMutation({ mutationFn: createConversation });

export const useDeleteConversation = () => useMutation({ mutationFn: deleteConversation });